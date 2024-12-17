from pyparsing import Word, alphas, Suppress, Combine, nums, string, Regex, Optional

from datetime import datetime

class Parser(object):
    # log lines don't include the year, but if we don't provide one, datetime.strptime will assume 1900
    ASSUMED_YEAR = str(datetime.today().year)

    def __init__(self):
        ints = Word(nums)

        # priority
       # priority = Suppress("<") + ints + Suppress(">")

        # timestamp
        month = Word(string.ascii_uppercase, string.ascii_lowercase, exact=3)
        day   = ints
        hour  = Combine(ints + ":" + ints + ":" + ints)

        timestamp = month + day + hour
        # a parse action will convert this timestamp to a datetime
        timestamp.setParseAction(lambda t: datetime.strptime(Parser.ASSUMED_YEAR + ' ' + ' '.join(t), '%Y %b %d %H:%M:%S'))

        # hostname
        hostname = Word(alphas + nums + "_-.")

        # appname
        appname = Word(alphas + "/-_.()")("appname") + (Suppress("[") + ints("pid") + Suppress("]")) | (Word(alphas + "/-_.")("appname"))
        appname.setName("appname")

        # message
        message = Regex(".*")

        # pattern build
        # (add results names to make it easier to access parsed fields)
        self._pattern = timestamp("timestamp") + hostname("hostname") + Optional(appname) + Suppress(':') + message("message")

    def parse(self, line):
        parsed = self._pattern.parseString(line)
        # fill in keys that might not have been found in the input string
        # (this could have been done in a parse action too, then this method would
        # have just been a two-liner)
        for key in 'appname pid'.split():
            if key not in parsed:
                parsed[key] = ''
        return parsed.asDict()
    

pattern = Parser()

tests = """\
Mar  7 04:02:16 avas clamd[11165]: /var/amavis/amavis-20040307T033734-10329/parts/part-00003: Worm.Mydoom.F FOUND 
Mar  7 04:05:55 avas clamd[11240]: /var/amavis/amavis-20040307T035901-10615/parts/part-00002: Worm.SomeFool.Gen-1 FOUND 
Mar  7 09:00:51 avas clamd[27173]: SelfCheck: Database status OK.
Mar  7 05:59:02 avas clamd[27173]: Database correctly reloaded (20400 viruses) 
Mar  7 11:14:35 avas dccd[13284]: 21 requests/sec are too many from anonymous 205.201.1.56,2246
Mar  8 00:22:57 avas dccifd[9933]: write(MTA socket,4): Broken pipe
Mar  7 21:23:22 avas dccifd[6191]: missing message body
Mar  9 16:05:17 avas named[12045]: zone PLNet/IN: refresh: non-authoritative answer from master 10.0.0.253#53
Mar 10 00:38:16 avas dccifd[23069]: continue not asking DCC 17 seconds after failure
Mar 10 09:42:11 avas named: client 127.0.0.1#55524: query: 23.68.27.142.sa-trusted.bondedsender.org IN TXT
Mar  9 03:48:07 avas dccd[145]: automatic dbclean; starting `dbclean -DPq -i 1189 -L info,local5.notice -L error,local5.err`
Mar  9 11:58:18 avas kernel: i810_audio: Connection 0 with codec id 2
Mar  9 19:41:13 avas dccd[3004]: "packet length 44 too small for REPORT" sent to client 1 at 194.63.250.215,47577
Mar  8 09:01:07 avas sshd(pam_unix)[21839]: session opened for user tom by (uid=35567)
Mar  8 03:52:04 avas dccd[13284]: 1.2.32 database /home/dcc/dcc_db reopened with 997 MByte window
Mar  8 16:05:26 avas arpwatch: listening on eth0
Mar 10 10:00:06 avas named[6986]: zone PLNet/IN: refresh: non-authoritative answer from master 192.75.26.21#53
Mar 10 10:00:10 avas named[6986]: client 127.0.0.1#55867: query: mail.canfor.ca IN MX
Mar  8 15:18:40 avas: last message repeated 11 times"""

print(pattern.parse(tests))