#!/usr/bin/env python3
"""
YouTube Video Downloader
برای استفاده شخصی - لطفاً از حقوق صاحبان محتوا احترام کنید
"""

import sys
import os
from pathlib import Path
import yt_dlp


def download_video(url, output_path="downloads"):
    """
    دانلود ویدیو از یوتیوب
    
    Args:
        url: لینک ویدیو یوتیوب
        output_path: مسیر ذخیره فایل
    """
    # ساخت پوشه خروجی
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # تنظیمات دانلود
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [progress_hook],
        # محدودیت سرعت (اختیاری - برای جلوگیری از مسدود شدن)
        # 'ratelimit': 1000000,  # 1MB/s
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🎬 شروع دانلود: {url}")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"✅ دانلود کامل شد: {filename}")
            return filename
    except Exception as e:
        print(f"❌ خطا در دانلود: {str(e)}", file=sys.stderr)
        sys.exit(1)


def progress_hook(d):
    """نمایش پیشرفت دانلود"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"📥 دانلود: {percent} | سرعت: {speed} | زمان باقیمانده: {eta}", end='\r')
    elif d['status'] == 'finished':
        print("\n🔄 در حال پردازش فایل...")


def main():
    """تابع اصلی"""
    if len(sys.argv) < 2:
        print("❌ لطفاً لینک ویدیو را وارد کنید")
        print("استفاده: python download.py <youtube_url>")
        sys.exit(1)
    
    video_url = sys.argv[1]
    
    # بررسی اعتبار URL
    if not ('youtube.com' in video_url or 'youtu.be' in video_url):
        print("⚠️  هشدار: این لینک شبیه یوتیوب نیست")
    
    download_video(video_url)


if __name__ == "__main__":
    main()
