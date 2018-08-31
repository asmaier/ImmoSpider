import smtplib
from scrapy import signals


class SendMail(object):

	def __init__(self, fromaddr, to, smtp_server, user, password):
		self.fromaddr = fromaddr
		self.toaddr = to
		self.smtp_server = smtp_server
		self.user = user
		self.password = password
		self.items = []

	@classmethod
	def from_crawler(cls, crawler):

		settings = crawler.settings
		fromaddr = settings.get("FROM")
		toaddr = settings.get("TO")
		smtp_server = settings.get("SMTP")
		user = settings.get("USER")
		password = settings.get("PASS")
        	
		ext = cls(fromaddr, toaddr, smtp_server, user, password)

		crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
		crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
		
		return ext

	def spider_closed(self, spider):

		if len(self.items) > 0: 

			message = "Hello from Immüspider\r\n"
			# message+= "\r\n".join([str(item) for item in self.items])				

			msg = "\r\n".join([
				"From: " + self.fromaddr,
				"To: " + self.toaddr,
				"Subject: New Items from Immospider",
				message
				])
			
			print(msg)

			server = smtplib.SMTP(self.smtp_server)
			server.ehlo()
			server.starttls()
			server.login(self.user, self.password)
			server.sendmail(self.fromaddr, self.toaddr, msg.encode("utf8"))
			server.quit()	

	def item_scraped(self, item, spider):
		self.items.append(item)

