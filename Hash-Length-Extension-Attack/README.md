# SEEDLAB: Hash Length Extension Attack


### 題目網址
https://seedsecuritylabs.org/Labs_20.04/Files/Crypto_Hash_Length_Ext/Crypto_Hash_Length_Ext.pdf

### Task1
這題是要我們將自己名子(henry)加到url的myname參數裡，並且從key.txt挑選其中一個uid(1002)與其對應的key(983abe)加入url的參數，並透過將圖中"983....lstcmd=1"的參數進行雜湊後得到得值，加進url的mac參數，最後對伺服器發出請求就會得到如圖中"Yes,your MAC is valid"的訊息。
![](https://hackmd.io/_uploads/rkkgU-pEh.png)


### Task2
本題是要我們將url的參數進行padding成64bytes符合RFC 6234標準對於SHA256的規範。
```
/* 我的URL參數，長度為37bytes */
983abe:myname=henry&uid=1002&lstcmd=1
```
```
/* padding，總長度為27bytes，最後是37*8 = 296(dec) = 128(hex) */
%80
%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00
%01%28
```
### Task3 

* step1 產生新的MAC
```
/* length_ext.c */

 // 替換成自己的MAC
 c.h[0] = htole32(0x787a006d);
 c.h[1] = htole32(0xc8d4d306);
 c.h[2] = htole32(0x43537118);
 c.h[3] = htole32(0xb8b686fa);
 c.h[4] = htole32(0x342eaf79);
 c.h[5] = htole32(0x1da06caa);
 c.h[6] = htole32(0xc81f940f);
 c.h[7] = htole32(0xb9bacbf9);


 // 添加payload
 SHA256_Update(&c, "&download=secret.txt", 20);
```

* step2 使用帶有payload的url對sever進行請求
```
http://www.seedlab-hashlen.com/?983abe:myname=henry&uid=1002&lstcmd=1%80
%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%01%28&download=secret.txt&mac=7bab16ddbf6b8f93f546d9c5c45d62a4d32b5d49a7cfef36102dca6276f67598
```


* step3 得到TOP SECRET
![](https://hackmd.io/_uploads/SyDEbXp43.png)


## Task4

修改server的程式碼
```

def verify_mac(key, my_name, uid, cmd, download, mac):
    download_message = '' if not download else '&download=' + download
    message = ''
    if my_name:
        message = 'myname={}&'.format(my_name)
    message += 'uid={}&lstcmd='.format(uid) + cmd + download_message
    payload = key + ':' + message
    app.logger.debug('payload is [{}]'.format(payload))
    
    # 以下已改成hmac
    real_mac = hmac.new(bytearray(key.encode('utf-8')),msg=message.encode('utf-8', 'surrogateescape'),digestmod=hashlib.sha256).hexdigest()


    app.logger.debug('real mac is [{}]'.format(real_mac))
    if mac == real_mac:
        return True
    return False

```
重新build server後發現原本的攻擊失效了!

![](https://hackmd.io/_uploads/SJQXdm6E3.png)
HMAC可以預防hash length extension attack最重要的特點是多了把key。
HMAC確保在沒有key的情況下，即使攻擊者知道MAC和被攔截到的URL參數，也無法得出合法的MAC。
