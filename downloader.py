import os
import asyncio
import aiohttp
import aiofiles
from yandex_music import Client
import time
from logger import success, warning, error, info, track, debug


async def get_track_info(client, like, index: int, semaphore):
    async with semaphore:
        try:
            track_id = f"{like.id}:{like.album_id}"
            track_obj = await asyncio.get_event_loop().run_in_executor(
                None, lambda: client.tracks(track_id)[0]
            )
            
            artist_name = track_obj.artists[0].name if track_obj.artists else "Unknown"
            track_title = track_obj.title
            
            filename = f"{index:03d}_{artist_name} - {track_title}.mp3"
            filename = "".join(c for c in filename if c not in '<>:"/\\|?*')
            
            download_info = await asyncio.get_event_loop().run_in_executor(
                None, lambda: track_obj.get_download_info(get_direct_links=True)
            )
            
            best_quality = None
            for info_item in download_info:
                if info_item.codec == 'mp3':
                    if best_quality is None or info_item.bitrate_in_kbps > best_quality.bitrate_in_kbps:
                        best_quality = info_item
            
            if not best_quality:
                return None
            
            if not best_quality.direct_link:
                download_data = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: client.request.retrieve(best_quality.download_info_url)
                )
                download_url = download_data.get('src') if isinstance(download_data, dict) else None
            else:
                download_url = best_quality.direct_link
            
            if not download_url:
                return None
            
            return {
                'filename': filename,
                'download_url': download_url,
                'artist': artist_name,
                'title': track_title,
                'bitrate': best_quality.bitrate_in_kbps,
                'index': index
            }
            
        except Exception as e:
            return None

async def download_track(session, track_info, download_dir, total_tracks, semaphore, logger, counter):
    if not track_info:
        return False
        
    filepath = os.path.join(download_dir, track_info['filename'])
    
    if os.path.exists(filepath):
        counter['completed'] += 1
        logger.info(f"[{counter['completed']}/{total_tracks}] Pass {track(track_info['artist'])} - {track_info['title']}")
        return True
    
    async with semaphore:
        try:
            start_time = time.time()
            async with session.get(track_info['download_url']) as response:
                if response.status != 200:
                    return False
                    
                async with aiofiles.open(filepath, 'wb') as f:
                    async for chunk in response.content.iter_chunked(131072):
                        if chunk:
                            await f.write(chunk)

                download_time = time.time() - start_time
                file_size = os.path.getsize(filepath)
                speed = file_size / 1024 / 1024 / download_time if download_time > 0 else 0
                
                counter['completed'] += 1
                logger.info(f"[{counter['completed']}/{total_tracks}] {success('Success')} {track(track_info['artist'])} - {track_info['title']} ({info(f'{speed:.1f} MB/s')})")
                return True
                
        except Exception as e:
            counter['completed'] += 1
            logger.info(f"[{counter['completed']}/{total_tracks}] Error {error('Error:')} {track(track_info['artist'])} - {track_info['title']}")
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
            return False

async def download_all_tracks(token, download_dir, logger):
    start_time = time.time()
    
    client = Client(token).init()
    
    likes = client.users_likes_tracks()
    if not likes or not likes.tracks:
        return
    
    total_tracks = len(likes.tracks)

    max_concurrent_info = 5
    max_concurrent_downloads = 3
    
    info_semaphore = asyncio.Semaphore(max_concurrent_info)
    download_semaphore = asyncio.Semaphore(max_concurrent_downloads)
    
    counter = {'completed': 0}
    
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=300, sock_connect=30, sock_read=60)
    ) as session:
        
        info_tasks = [
            get_track_info(client, like, i, info_semaphore) 
            for i, like in enumerate(likes.tracks, 1)
        ]
        
        download_tasks = set()
        
        for future in asyncio.as_completed(info_tasks):
            track_info = await future
            
            if track_info:
                download_task = asyncio.create_task(
                    download_track(session, track_info, download_dir, total_tracks, download_semaphore, logger, counter)
                )
                download_tasks.add(download_task)
                
                if len(download_tasks) >= max_concurrent_downloads:
                    done, download_tasks = await asyncio.wait(
                        download_tasks, 
                        return_when=asyncio.FIRST_COMPLETED
                    )
        
        if download_tasks:
            await asyncio.wait(download_tasks)