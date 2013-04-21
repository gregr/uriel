# Gregory Rosenblatt
# 12/16/05

from twisted.python import log
import sys

def LogAck(ack):
	"""Log a relevant acknowledgement of a successful deferred call."""
	if ack is not None:
		log.msg("Acknowledged: %s" % ack)

def LogErr(error):
	"""Log an error message if a deferred call fails."""
	log.err("%s - %s" % (error.getErrorMessage(), error.type))

log.startLogging(sys.stdout, setStdout=False)	# log to stdout by default
