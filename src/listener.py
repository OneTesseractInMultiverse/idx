from log_management.syslog_impl import DefaultLogger
from log_management.interfaces import MicroserviceLogger
from messaging import AbstractNATSSubscriber
from operators import IdentityOperation
from db_connection import get_db
import asyncio
import json
import settings


# -----------------------------------------------------------------------------
# CLASS SAMPLE HANDLER
# -----------------------------------------------------------------------------
class IdentityEventHandler(AbstractNATSSubscriber):

    # -------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -------------------------------------------------------------------------
    def __init__(self,
                 event_loop: asyncio.AbstractEventLoop,
                 logger: MicroserviceLogger,
                 subject: str,
                 queue: str
                 ):
        super().__init__(
            event_loop,
            logger,
            subject,
            queue
        )

    # -------------------------------------------------------------------------
    # METHOD MESSAGE HANDLER
    # -------------------------------------------------------------------------
    async def message_handler(self, message):
        self._logger.info(
            message.data.decode()
        )
        print(f"Reply subject: {message.reply}")

        await self.send_reply(
            json.dumps(IdentityOperation(
                logger=self._logger,
                db_provider_func=get_db,
                message=message
            ).exec()),
            message.reply
        )


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    client = IdentityEventHandler(
        event_loop=loop,
        logger=DefaultLogger(),
        subject=settings.NATS_SUBJECT,
        queue=settings.NATS_QUEUE
    )
    loop.run_until_complete(client.start())
    try:
        loop.run_forever()
    finally:
        loop.close()
