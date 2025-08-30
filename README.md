# ACYBER-Wayback-Machine-Downloader
A powerful Python tool for downloading historical files (PDF, JPG, PNG, CSS, JS, etc.) from the Internet Archive Wayback Machine with support for SOCKS5 proxies, retry logic, random User-Agent rotation, and colored terminal output.

Features:  
- Fetch snapshots from Wayback Machine  
- Download files by extension (pdf, jpg, png, css, js, ...)  
- SOCKS5 proxy support (port range scanning)  
- Random User-Agent rotation for each request  
- Robust error handling with retries and delays  
- Colorized and human-readable console output  

# Proxy Usage

If you **don’t need a proxy**, simply omit the `-proxyport` option.  
```bash
python downloader.py -url example.com -type pdf
```
If you have a single proxy port, provide it directly:
```bash
python downloader.py -url example.com -type pdf -proxyport 1080-1080
```
If you want to use multiple proxies in a range, specify the range (e.g., 1080–1090):
```bash
python downloader.py -url example.com -type pdf -proxyport 1080-1090
```


# Arguments:
- url → Domain or URL (e.g., example.com)
- type → File type/extension (e.g., pdf, jpg, png, css, js)
- proxyport → SOCKS5 proxy port range (e.g., 1080-1090)
# Output:
- Files are saved in the current working directory.
- Filenames are formatted as {timestamp}_{original_filename}.{ext}
- Already downloaded files are skipped with [SKIP].

## Disclaimer:
This tool is intended for research, data recovery, and educational purposes only. Please use responsibly and in compliance with applicable laws and archive.org terms of service.
