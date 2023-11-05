async def _change_metadata(event):
        chat_id = event.message.chat.id
        user_id = event.message.sender.id
        command = '/changemetadata'
        if user_id not in get_data():
                await new_user(user_id, SAVE_TO_DATABASE)
        link, custom_file_name = await get_link(event)
        if link=="invalid":
            await event.reply("❗Invalid link")
            return
        elif not link:
            new_event = await ask_media_OR_url(event, chat_id, user_id, [command, "stop"], "Send Video or URL", 120, "video/", True)
            if new_event and new_event not in ["cancelled", "stopped"]:
                link = await get_url_from_message(new_event)
            else:
                return
        metadata_event = await ask_text_event(chat_id, user_id, event, 120, "Send Metadata", message_hint="🔷`a` Is For Audio & `s` Is For Subtitle\n🔷 Send In The Format As Shown Below:\n\n`a:0-AudioLanguage-AudioTitle` (To Change Audio Number 1 Metadata)\n`s:0-SubLanguage-SubTitle` (To Change Subtitle Number 1 Metadata)\n\n`v:VideoTitle` (To Change Video Title)\n\nFor example: `v:MyAwesomeVideo`")
        if not metadata_event:
            return
        custom_metadata_list = str(metadata_event.message.message).split('\n')
        custom_metadata = []
        video_title = ""

        for m in custom_metadata_list:
            mdata = str(m).strip().split('-')
            LOGGER.info(mdata)

            if mdata[0].lower().startswith('v'):  # Video title metadata
                 video_title = str(mdata[0][2:])  # Extract video title
            else:
                try:
                    sindex = str(mdata[0]).strip().lower()
                    mlang =  str(mdata[1]).lower()
                    mtilte = str(mdata[2])
                    custom_metadata.append([f'-metadata:s:{sindex}', f"language={mlang}", f'-metadata:s:{str(sindex)}', f"title={mtilte}"])
                except Exception as e:
                    await metadata_event.reply(f"❗Invalid Metadata, Error: {str(e)}")
                    return
        user_name = get_username(event)
        user_first_name = event.message.sender.first_name
        process_status = ProcessStatus(user_id, chat_id, user_name, user_first_name, event, Names.changeMetadata, custom_file_name, custom_metadata=custom_metadata, video_title=video_title)
        task = {}
        task['process_status'] = process_status
        task['functions'] = []
        if type(link)==str:
                task['functions'].append(["Aria", Aria2.add_aria2c_download, [link, process_status, False, False, False, False]])
        else:
            task['functions'].append(["TG", [link]])
        await get_thumbnail(process_status, [command, "pass"], 120)
        create_task(add_task(task))
        await update_status_message(event)
        return
