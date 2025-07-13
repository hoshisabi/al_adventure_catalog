map(select(.hours == 2 and .campaign == "Forgotten Realms")) | 
.[] | 
[.code, .full_title, .hours, .tiers, .campaign, .url] | 
join(",")
