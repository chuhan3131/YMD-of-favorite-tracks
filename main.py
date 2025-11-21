import os
import sys
import time
import asyncio
import argparse
from yandex_music import Client

from downloader import download_all_tracks
from logger import setup_logger, success, warning, error, info, track

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Yandex.Music downloader of your favorite tracks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
  {sys.argv[0]} --token "your_token"
  {sys.argv[0]} -t "your_token" -d "your_dir_for_download"

  Instructions for obtaining a Yandex.Music token -
        '''
    )
    
    parser.add_argument(
        '-t', '--token', '--ym', '--musictoken',
        dest='token',
        type=str,
        required=True,
        help='Yandex.Music token (required)'
    )
    
    parser.add_argument(
        '-d', '--directory', '--dir',
        dest='directory',
        type=str,
        default='downloads',
        help='Download folder (default: downloads)'
    )
    
    return parser.parse_args()

def validate_arguments(args):
    errors = []
    
    if not args.token.strip():
        errors.append("Token cannot be empty!")
    
    return errors

async def main():
    args = parse_arguments()
    
    errors = validate_arguments(args)
    if errors:
        print("Errors in arguments:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    logger = setup_logger()
    
    os.makedirs(args.directory, exist_ok=True)
    
    try:
        client = Client(args.token).init()
        user_info = client.me
        
        likes = client.users_likes_tracks()
        if not likes or not likes.tracks:
            logger.info(f"{error('No favorite tracks')}")
            return
        
        total_tracks = len(likes.tracks)
        
        logger.info(f"Logged in as: {info(user_info.account.login)}")
        logger.info(f"Total tracks: {info(total_tracks)}")
        logger.info(f"Folder: {info(args.directory)}")
        
        start_time = time.time()

        await download_all_tracks(
            token=args.token,
            download_dir=args.directory,
            logger=logger
        )

        end_time = time.time()
        total_time = end_time - start_time

        logger.info(f"{success(f'Download completed successfully in {total_time:.2f} seconds!')}")

                
    except KeyboardInterrupt:
        logger.info(f"{warning('Download interrupted by user')}")
    except Exception as e:
        logger.error(f"{error(f'Critical error: {e}')}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())