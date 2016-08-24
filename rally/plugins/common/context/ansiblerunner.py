from rally.common import ansibleutils as ansible
from rally import consts
from rally.task import context


@context.configure(name="ansible", order=100)
class AnsibleRunner(context.Context):
    """Run ansible playbook on the start and on the end of scenario."""

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "additionalProperties": False,
        "properties": {
            "playbook_on_start": {
                "type": "string",
            },
            "playbook_on_end": {
                "type": "string",
            },
            "hosts_file": {
                "type": "string",
            }
        }
    }

    def _run_playbook(self, playbook, hosts_file):
        runner = ansible.Runner(
            playbook=playbook,
            hosts=hosts_file,
            options={
                "connection": "ssh",
                "become": True,
                "become_method": "sudo",
                "become_user": "root",
                # "private_key_file": "/path/to/the/id_rsa",
                # "tags": "debug",
                # "skip_tags": "debug",
                # "verbosity": 3,
            },
                # passwords={
                #     "become_pass": "sudo_password",
                #     "conn_pass": "ssh_password",
                # },
                # vault_pass="vault_password",
        )

        runner.run()

    def setup(self):
        if self.config.get("playbook_on_start"):
            self._run_playbook(
                self.config.get("playbook_on_start"),
                self.config.get("hosts_file")
            )

    def cleanup(self):
        if self.config.get("playbook_on_end"):
            self._run_playbook(
                self.config.get("playbook_on_end"),
                self.config.get("hosts_file")
            )
