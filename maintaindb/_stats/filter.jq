map(select(.hours < 2)) | 
.[] | 
[.code, .full_title, .hours, .tiers, .campaign, .url] | 
join(",")
