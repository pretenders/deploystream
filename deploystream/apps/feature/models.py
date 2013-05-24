from collections import defaultdict


class Feature(object):
    """
    The class used for encapsulating ``Feature`` data across repos & branches.

    It contains planning information obtained from a management tool.
    An internal convenience class, instances of which are intended to be
    exposed via the API to front end clients.

    Instances of this class contain:

        ``provider``        - The provider that provided all of these values.
        ``project``         - The project where this feature belongs.
        ``id``              - The id of the feature.
        ``title``           - The name of the feature.
        ``type``            - The type of the feature.
        ``owner``           - The owner of the feature.
        ``description``     - Long description of the feature.
        ``url``             - The url to the feature.

        ``branches``        - a list of ``Branch`` objects

        ``trees``           - A tree of how the branches in ``branches`` relate
                              to one another. This will be especially useful at
                              the front end to display information about what
                              branches are merged into their parents etc.
    """
    def __init__(self, provider, project, id, title,
                 type='story', owner=None, description=None, url=None,
                 **kwargs):
        self._provider = provider
        self.provider = getattr(provider, 'name', provider.__class__.__name__)
        self.project = project
        self.id = id
        self.title = title
        self.type = type
        self.owner = owner
        self.description = description
        self.url = url
        self._extras = kwargs

        self.branches = defaultdict(dict)
        self.trees = []

    def add_branch(self, branch):
        assert isinstance(branch, Branch)
        self.branches[branch.repo_name][branch.branch_name] = branch

    def create_hierarchy_trees(self):
        "Create hierarchy trees - one for each repo."
        for branch_set in self.branches.values():
            for branch in branch_set.values():
                if branch.parent_branch_name:
                    branch.parent = branch_set[branch.parent_branch_name]


class Branch(object):
    """
    A class to encapsulate information to do with a single branch on a repo.

    Instances contain values for:

        ``repo_name``           - The repository that this branch is found in.
        ``branch_name``         - The name of the branch.
        ``latest_commit``       - The head commmit, or latest revision in this
                                  branch.
        ``parent_branch_name``  - The name of the branches parent.
        ``provider``            - The provider instance that found this branch
                                  information.


    Instances are eventually populated with these values:

        ``build_info``    - Build information for this particular branch.

        ``parent``        - The parent ``Branch`` of this branch (based on
                            hierarchy rules)
        ``children``      - A list of children ``Branch`` es of this branch.

    """

    def __init__(self, repo_name, branch_name, latest_commit,
                 parent_branch_name, provider):
        self._parent = None
        self.children = []
        self.build_info = None
        self.repo_name = repo_name
        self.branch_name = branch_name
        self.latest_commit = latest_commit
        self.parent_branch_name = parent_branch_name
        self._provider = provider

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, branch):
        if self._parent:
            # remove first
            self._parent.remove_child(self)
        self._parent = branch
        branch.ensure_child(self)

    def ensure_child(self, branch):
        if branch not in self.children:
            self.children.append(branch)

    def remove_child(self, branch):
        try:
            self.children.remove(branch)
        except ValueError:
            pass

    def as_tree_string(self, indent=0):
        if self.parent and not indent:
            return self.parent.as_tree_string()
        me = "{0}- {1}\n".format(indent * ' ', self.branch_name)

        for c in self.children:
            me += c.as_tree_string(indent + 4)
        return me


class BuildInfo(object):
    """
    A class encapsulating build information from an CI tool.

    Instances of this class contain values for:

        ``timestamp``       - A ``datetime`` timestamp of the time of built.
        ``result``          - The result of the build. Currently one of
                              "success", "failure", "unstable", "partial".
                              TODO:
                              Validate these from provider and convert to
                              internal constants as per @txels request :)
        ``commit``          - The commit or revision built.
        ``url``             - The url to the results of the build.
        ``provider``        - The provider that provided all of these values.
    """

    def __init__(self, timestamp, result, commit, url, provider):
        self.timestamp = timestamp
        self.result = result
        self.commit = commit
        self.url = url
        self._provider = provider
