alarm_cmsd.py creates alarm for CPU, Memory, SWAP, DISK, It will be alarm if one of them is more than 80%.

monitor_activelog.py monitors line of activeLog.log and pushes line number to cloudwatch.
alarm_activelog.py can create alarm for line number of activeLog.log. It will be alarm if the line number of file is more than 200.


monitor_files_acp.py pushes data to cloudwatch for requestAdserver.log, requestClick.log and requestPixel.log. It pushes 1 to cloudwatch if the file is exist, else it will push 0. It also pushes line number of file to cloudwatch for three files.
alarm_files_acp.py creates alarm for exist and line number for requestAdserver.log, requestClick.log and requestPixel.log.It will be alarm if the size of file is less than 20 bytes. It will be alarm if the value of file equals 0. It will be alarm if the line number of file is less than 1.


monitor_files_cccps.py pushes line number to cloudwatch for cacheUpdater.log, cleaner.log, creativeUpdater.log, pixelUpdater.log and sender.log.
alarm_files_cccps.py creates alarm for line number of every file. It will be alarm if the line number of file is less than 20.


monitor_hadoop_file.py pushes file size to cloudwatch for current day about bucket hadoop.anonymous.com.
alarm_hadoop_file.py creates alarm for file size. It will be alarm if file size is less than 20 bytes.
vo_hadoop_file.py is a VO file. it can set/get name and size for file attribute.
The following folder that is monitored:
hadoop.anonymous.com/output/click_count_day
hadoop.anonymous.com/output/country_creative_day
hadoop.anonymous.com/output/creative_camp_day
hadoop.anonymous.com/output/creative_camp_hourly
hadoop.anonymous.com/output/creative_url_camp_day
hadoop.anonymous.com/output/dma_creative_day
hadoop.anonymous.com/output/dma_pixel_day
hadoop.anonymous.com/output/event_count_day
hadoop.anonymous.com/output/event_count_day
hadoop.anonymous.com/output/event_count_increment
hadoop.anonymous.com/output/impression_count_day
hadoop.anonymous.com/output/pcc
hadoop.anonymous.com/output/pvc
hadoop.anonymous.com/output/revenue_count_day
hadoop.anonymous.com/output/url_camp_day
hadoop.anonymous.com/output/url_domain_day
hadoop.anonymous.com/output/watched_video_count_day
hadoop.anonymous.com/output/xch_line_creative_click_count_day
hadoop.anonymous.com/output/xch_line_creative_impression_count_day
hadoop.anonymous.com/output/xch_line_creative_revenue_count_day
hadoop.anonymous.com/output/xch_line_creative_watched_video_count_day


alarm_email_sender can send alarm situations by email every hour.

