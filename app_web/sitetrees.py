from django.utils.translation import gettext_lazy as _
from sitetree.sitetreeapp import compose_dynamic_tree, register_dynamic_trees
from sitetree.utils import tree, item

sitetrees = [
    tree("main", items=[
        item(_("Home"), "index"),
        item(_("Privacy"), "imprint"),
        item(_("Imprint"), "imprint"),
    ]),
]

register_dynamic_trees(
    compose_dynamic_tree("core"),
)
