unset num
defpasswd="password"
#hard code the hostname, ip and octets below:
for i in {114..122};do 
  ip="10.64.144.$i"
  num=$((num+1))
  host="myhostname-"$num
  echo $ip $host $defpasswd
./setup_new_rack_expect $ip $host $defpasswd
done

