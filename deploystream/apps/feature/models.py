class Feature(object):
    """
    The class used for encapsulating ``Feature`` data across repos & branches.

    An internal convenience class, instances of which are intended to be
    exposed via the API to front end clients.

    Instances of this class contain:

        ``plugin``        - the plugin where this issue came from.

        ``id``            - the feature identifier.

        ``branches``      - a list of ``Branch`` objects

        ``planning_info`` - an instance of ``PlanningInfo`` or ``None`` if not
                            available.

        ``trees``         - A tree of how the branches in ``branches`` relate
                            to one another. This will be especially useful at
                            the front end to display information about what
                            branches are merged into their parents etc.
    """
    def __init__(self, plugin, id):
        self._plugin = plugin
        self.id = id
        self.branches = []
        self.planning_info = None
        self.trees = []

    def create_hierarchy_trees(self, regexes):
        "Create hierarchy trees - one for each repo."
        pass

    def add_branch(self, branch):
        assert isinstance(branch, Branch)
        self.branches.append(branch)


class PlanningInfo(object):
    """
    A class encapsulating planning information from a management tool.

    Instances of this class contain values for:

        ``title``           - The name of the feature.
        ``id``              - The id of the feature.
        ``url``             - The url to the feature.
        ``feature_type``    - The type of the feature.
        ``owner``           - The owner of the feature.
        ``description``     - Long description of the feature.
        ``plugin``          - The plugin that provided all of these values.
    """

    def __init__(self, plugin, id, title, feature_type='story',
                 owner=None, description=None, url=None, **kwargs):
        self.title = title
        self.id = id
        self.url = url
        self.feature_type = feature_type
        self.owner = owner
        self.description = description
        self._plugin = plugin
        self.extras = kwargs


class Branch(object):
    """
    A class to encapsulate information to do with a single branch on a repo.

    Instances contain values for:

        ``repo_name``     - The repository that this branch is found in.
        ``branch_name``   - The name of the branch.
        ``latest_commit`` - The head commmit, or latest revision in this
                            branch.
        ``plugin``        - The plugin instance that found this branch
                            information.

    Instances are eventually populated with these values:

        ``build_info``    - Build information for this particular branch.

        ``parent``        - The parent ``Branch`` of this branch (based on
                            hierarchy rules)
        ``children``      - A list of children ``Branch`` es of this branch.
        ``siblings``      - A list of the sibling ``Branch`` es of this branch.
                            A sibling is a ``Branch`` that has the same parent,
                            or would have the same parent if one existed.
    """

    def __init__(self, repo_name, branch_name, latest_commit, plugin):
        self.parent = None
        self.children = []
        self.siblings = []  # Will be needed in the cases where we have no
                            # parent
        self.build_info = None
        self.repo_name = repo_name
        self.branch_name = branch_name
        self.latest_commit = latest_commit
        self._plugin = plugin


class BuildInfo(object):
    """
    A class encapsulating build information from an CI tool.

    Instances of this class contain values for:

        ``timestamp``       - A ``datetime`` timestamp of the time of built.
        ``result``          - The result of the build. Currently one of
                              "success", "failure", "unstable", "partial".
                              TODO:
                              Validate these from plugin and convert to
                              internal constants as per @txels request :)
        ``commit``          - The commit or revision built.
        ``url``             - The url to the results of the build.
        ``plugin``          - The plugin that provided all of these values.
    """

    def __init__(self, timestamp, result, commit, url, plugin):
        self.timestamp = timestamp
        self.result = result
        self.commit = commit
        self.url = url
        self._plugin = plugin
