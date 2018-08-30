import smtplib
from scrapy import signals

class SendMail(object):
	def __init__(self, from, to, smtp_server, user, pass):
		self.fromaddr = from
		self.toaddr = to
		self.smtp_server = smtp_server
		self.user = user
		self.pass = pass
		self.items = []

	@classmethod
	def from_crawler(cls, crawler):

		settings = crawler.settings
        	from = settings.get("FROM")
		to = settings.get("TO")
		smtp_server = settings.get("SMTP")
		user = settings.get("USER")
		pass = settings.get("PASS")
        	
		ext = cls(from, to, smtp_server, user, pass)

		crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
		crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
		
		return ext

	def spider_closed(self, spider):

		message = "\r\n".join(self.items)		

		msg = "\r\n".join([
			"From: " + self.fromaddr,
			"To: " + self.toaddr,
			"Subject: New Items from Immospider"
			message
			])
		
		server = smtplib.SMTP(self.smtp_server)
		server.ehlo()
		server.starttls()
		server.login(self.user, self.pass)
		server.sendmail(self.fromaddr, self.toaddr, msg)
		server.quit()	

	def item_scraped(self, item, spider):
        	self.items.append(item)
