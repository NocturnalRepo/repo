from ..plugin import Plugin
import xbmc, xbmcgui, xbmcaddon
import json
import resolveurl

addon_id = xbmcaddon.Addon().getAddonInfo('id')
default_icon = xbmcaddon.Addon(addon_id).getAddonInfo('icon')
default_fanart = xbmcaddon.Addon(addon_id).getAddonInfo('fanart')

def isList(item):
	if isinstance(item,list):
		return True
	else:
		return False

class default_play_video(Plugin):
    name = "default video playback"
    priority = 0

    def play_video(self, item):
        item = json.loads(item)
        link = item["link"]
        if isList(link):
        	if len(link) > 1:
        		labels = []
        		counter = 1
        		for x in link:
        			if x.strip().endswith(')'):
        				label = x.split('(')[-1].replace(')', '')
        			else:
        				label = 'Link ' + str(counter)
        			labels.append(label)
        			counter += 1		
       			dialog = xbmcgui.Dialog()
       			ret = dialog.select('Choose a Link', labels)
       			if ret == -1:
       				return
       			else:
       				if link[ret].strip().endswith(')'):
       					link = link[ret].rsplit('(')[0].strip()
       				else:
       					link = link[ret]
        	else:
        		if link[0].strip().endswith(')'):
        			link = link[0].rsplit('(')[0].strip()
        		else:
        			link = link[0]
        else:
        	link = item["link"]
        title = item["title"]
        thumbnail = item.get("thumbnail", default_icon)
        liz = xbmcgui.ListItem(title)
        liz.setInfo('video', {'Title': title})
        liz.setArt({'thumb': thumbnail, 'icon': thumbnail})
        if resolveurl.HostedMediaFile(link).valid_url():
        	url = resolveurl.HostedMediaFile(link).resolve()
        	return xbmc.Player().play(url,liz)
        else:
        	return xbmc.Player().play(link,liz)
       
       