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

        self.branches = []
        self.trees = []

    def create_hierarchy_trees(self):
        "Create hierarchy trees - one for each repo."
        pass

    def add_branch(self, branch):
        assert isinstance(branch, Branch)
        self.branches.append(branch)


class Branch(object):
    """
    A class to encapsulate information to do with a single branch on a repo.

    Instances contain values for:

        ``repo_name``     - The repository that this branch is found in.
        ``branch_name``   - The name of the branch.
        ``latest_commit`` - The head commmit, or latest revision in this
                            branch.
        ``level``         - The numerical level that this branch falls in the
                            hierarchy for the feature - where 0 is the highest
                            level.
        ``provider``      - The provider instance that found this branch
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

    def __init__(self, repo_name, branch_name, latest_commit, level, provider):
        self.parent = None
        self.children = []
        self.siblings = []  # Will be needed in the cases where we have no
                            # parent
        self.build_info = None
        self.repo_name = repo_name
        self.branch_name = branch_name
        self.latest_commit = latest_commit
        self.level = level
        self._provider = provider


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


class HierarchyNode(object):

    def __init__(self, level, repo, branch=None):
        self.children = []
        self._parent = None

        self.level = level
        self.repo = repo
        self.branch = branch

    def add_node(self, level, **kwargs):
        print "add_node", level, kwargs, self.level
        parent_level = level - 1
        if self.level == parent_level:
            # I am an appropriate parent
            print "adding {0} (level: {1}) to myself: ({2}, {3})".format(kwargs['branch'], level, self.branch, self.level)
            return self._add(level=level, **kwargs)
        elif self.level < parent_level:
            # There may be someone on a lower level more appropriate
            if self.children and self.children[0].level == parent_level:
                print "passing to child"
                self.children[0].add_node(level, **kwargs)
            else:
                print "adding {0} (level: {1}) to myself: ({2}, {3})".format(kwargs['branch'], level, self.branch, self.level)
                # I'm the best hope for the kid.
                return self._add(level=level, **kwargs)
        else:
            print "passing to parent"
            # I've got no right to father someone higher than me.
            return self.parent.add_node(level, **kwargs)

    def _add(self, **kwargs):
        print "ADDING as child of {0}".format(self.level)
        new_node = HierarchyNode(**kwargs)
        new_node.parent = self
        for child in self.children:
            # TODO: this actually needs to do more than this to move the item
            # further down the chain
            if child.level > new_node.level:
                child.parent = new_node
        print "children are now:", self.children, self.children[0].branch
        return new_node

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        if self._parent:
            # remove first
            self._parent.remove_child(self)
        self._parent = node
        node.ensure_child(self)

    def ensure_child(self, node):
        if node not in self.children:
            self.children.append(node)

    def remove_child(self, node):
        try:
            self.children.remove(node)
        except ValueError:
            pass

    def as_tree_string(self, indent=0):
        me = "{0}- {1}\n".format(indent * ' ', self.branch)
        if not self.branch:
            indent = -4
            me = ""

        for c in self.children:
            me += c.as_tree_string(indent + 4)
        return me


# class HierarchyTree(object):

#     def __init__(self, root_picker):
#         """
#         A hierarchy tree to link nodes to one another

#         :param root_picker:
#             An attribute to be expected on each node that decides which sub
#             tree to assign a node to. Eg "repository"
#         """
#         self.root_picker = root_picker
#         self.roots = defaultdict(lambda: HierarchyNode(-1))

#     def add_node(self, **kwargs):
#         return self.roots[kwargs[self.root_picker]].add_node(**kwargs)

#     def as_tree_string(self):
#         u = u''
#         for root_name, root in self.roots.items():
#             u += "Root: {0}\n".format(root_name)
#             u += root.as_tree_string(0)
#         return u
