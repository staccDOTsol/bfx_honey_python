var hosts='["","socks4://49.12.4.194:38523","socks4://178.150.237.227:4145","socks4://191.7.209.74:39383"]'
function FindProxyForURL(url, host){
return hosts}
console.log(FindProxyForURL('/', '0.0.0.0'))