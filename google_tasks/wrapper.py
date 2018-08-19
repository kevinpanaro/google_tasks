from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime


class GoogleTasksWrapper(object):
    def __init__(self, scopes="https://www.googleapis.com/auth/tasks",
                 credentials="credentials.json", token="token.json",
                 service_name="tasks", version="v1"):
        """
        initialize google tasks

        :param scopes: the scope of api (read/write or read)
        :param credentials: credentials json path/filename
        :param token: token json path/filename
        :param service_name: name of the service you're interacting with
        :param version: the api version number
        """
        self.scopes = scopes
        self.credentials = credentials
        self.token = token
        self.service_name = service_name
        self.version = version
        self.service = None
        self._update_token()
        self._obtain_current_lists()

    def add(self, tasklist, task, force=False, **kwargs):
        """
        adds an item to the task list

        :param tasklist: the tasklist name
        :param task: the todo task name
        """
        tasklist = self._get_tasklist_id(tasklist=tasklist, force=force)
        task = self._format_task_body(task=task, **kwargs)

        self.service.tasks().insert(tasklist=tasklist, body=task).execute()

    def get_current_lists(self):
        """
        returns the current lists
        """
        return(self.current_lists)

    def _update_token(self):
        """
        updates the token file and creates the service
        """
        store = file.Storage(self.token)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.credentials)
            creds = tools.run_flow(flow, store)
        self.service = build(self.service_name, self.version,
                             http=creds.authorize(Http()))

    def _delete_file(self, filename):
        pass

    def _obtain_current_lists(self):
        self.current_lists = self.service.tasklists().list().execute()

    def _format_task_body(self, task, **kwargs):
        """
        formats the task in the dict its supposed to be delivered in

        Example Output:
            {
              "status": "A String", # Status of the task. "needsAction" or "completed"
              "kind": "tasks#task", # Type of the resource. "tasks#task".
              "updated": "A String", # Last modification time of the task (as a RFC 3339 timestamp).
              "parent": "A String", # Parent task identifier. This field is omitted if it is a top-level task. This field is read-only. Use the "move" method to move the task under a different parent or to the top level.
              "links": [ # Collection of links. This collection is read-only.
                {
                  "type": "A String", # Type of the link, e.g. "email".
                  "link": "A String", # The URL.
                  "description": "A String", # The description. In HTML speak: Everything between <a> and </a>.
                },
              ],
              "title": "A String", # Title of the task.
              "deleted": True or False, # Flag indicating whether the task has been deleted. The default if False.
              "completed": "A String", # Completion date of the task (as a RFC 3339 timestamp). This field is omitted if the task has not been completed.
              "due": "A String", # Due date of the task (as a RFC 3339 timestamp). Optional.
              "etag": "A String", # ETag of the resource.
              "notes": "A String", # Notes describing the task. Optional.
              "position": "A String", # String indicating the position of the task among its sibling tasks under the same parent task or at the top level. If this string is greater than another task's corresponding position string according to lexicographical ordering, the task is positioned after the other task under the same parent task (or at the top level). This field is read-only. Use the "move" method to move the task to another position.
              "hidden": True or False, # Flag indicating whether the task is hidden. This is the case if the task had been marked completed when the task list was last cleared. The default is False. This field is read-only.
              "id": "A String", # Task identifier.
              "selfLink": "A String", # URL pointing to this task. Used to retrieve, update, or delete this task.
            }

        :param task: the task to format
        :param kwargs: incase the user wants to add notes
        """
        title = task
        status = kwargs.get("status", "needsAction")
        kind = kwargs.get("kind", "tasks#task")
        updated = kwargs.get("updated", self._utc_rfc3339())
        parent = kwargs.get("parent", None)
        deleted = kwargs.get("deleted", False)
        completed = kwargs.get("completed", None)
        due = kwargs.get("due", None)
        notes = kwargs.get("notes", None)
        hidden = kwargs.get("hidden", False)

        output = {"title": title,
                  "status": status,
                  "kind": kind,
                  "updated": updated,
                  "parent": parent,
                  "deleted": deleted,
                  "completed": completed,
                  "due": due,
                  "notes": notes,
                  "hidden": hidden}
        return(output)

    def _utc_rfc3339(self):
        d = datetime.utcnow()
        return(d.isoformat("T") + "Z")

    def _get_tasklist_id(self, tasklist, force=False):
        """
        get the tasklist id

        :param tasklist: the name of the task list
        :param force: bool to force creation of not
        """
        items = self.current_lists.get('items', [])

        for item in items:
            if item['title'] == tasklist:
                return(item['id'])
        else:
            if force:
                self._create_tasklist(tasklist)
                self._obtain_current_lists()
                return(self._get_tasklist_id(tasklist))
            else:
                raise NoSuchTaskList(f"\"{tasklist}\" does not exist.")

    def _create_tasklist(self, tasklist):
        """
        Called when a tasklist doesn't exist and creates it

        :param tasklist: the name of the tasklist
        """
        tasklist = self._format_tasklist(tasklist)
        self.service.tasklists().insert(body=tasklist).execute()

    def _format_tasklist(self, tasklist):
        """
        formats the task list body

        Example Output:
          {
            "kind": "tasks#taskList", # Type of the resource. This is always "tasks#taskList".
            "title": "A String", # Title of the task list.
            "updated": "A String", # Last modification time of the task list (as a RFC 3339 timestamp).
            "etag": "A String", # ETag of the resource.
            "id": "A String", # Task list identifier.
            "selfLink": "A String", # URL pointing to this task list. Used to retrieve, update, or delete this task list.
          }

        :param tasklist: the name of the tasklist
        """
        title = tasklist
        kind = "tasks#taskList"
        updated = self._utc_rfc3339()

        output = {"title": title,
                  "kind": kind,
                  "updated": updated,
                  }
        return(output)

class NoSuchTaskList(Exception):
    pass
