# vim: set fileencoding=utf-8
"""
pythoneda/runtime/secrets/secrets.py

This file declares the Secrets class.

Copyright (C) 2024-today rydnr's pythoneda-runtime/secrets

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.shared import (
    listen,
    EventListener,
)
from pythoneda.shared.runtime.events import (
    CredentialIssued,
    CredentialProvided,
    CredentialRequested,
)


class Secrets(EventListener):
    """
    A way to deal with Secrets in PythonEDA.

    Class name: Secrets

    Responsibilities:
        - Reacts to requests regarding credentials.

    Collaborators:
        - None
    """

    _singleton = None

    def __init__(self):
        """
        Creates a new Secrets instance.
        """
        super().__init__()
        self._live_credentials = {}

    @classmethod
    def instance(cls):
        """
        Retrieves the singleton instance.
        :return: Such instance.
        :rtype: pythoneda.runtime.Secrets
        """
        if cls._singleton is None:
            cls._singleton = cls.initialize()

        return cls._singleton

    @classmethod
    def initialize(cls):
        """
        Initializes the singleton instance.
        :return: Such instance.
        :rtype: pythoneda.runtime.Secrets
        """
        return cls()

    @classmethod
    @listen(CredentialIssued)
    async def listen_CredentialIssued(cls, event: CredentialIssued):
        """
        Gets notified of a CredentialIssued event.
        :param event: The event.
        :type event: pythoneda.shared.secrets.events.CredentialIssued
        """
        Secrets.logger().info(f"Received {event}")

        instance = cls.instance()

        instance._live_credentials[event.name] = event.value

    @classmethod
    @listen(CredentialRequested)
    async def listen_CredentialIssued(
        cls, event: CredentialRequested
    ) -> CredentialProvided:
        """
        Gets notified of a CredentialRequested event.
        :param event: The event.
        :type event: pythoneda.shared.secrets.events.CredentialRequested
        :return: A CredentialProvided event, or None if the credential is not available.
        :rtype: pythoneda.shared.secrets.events.CredentialProvided
        """
        result = None

        Secrets.logger().info(f"Received {event}")

        instance = cls.instance()

        instance._live_credentials[event.name] = event.value

        credential = instance._live_credentials.get(event.name, None)

        if credential is not None:
            result = CredentialProvided(event.name, credential)

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
