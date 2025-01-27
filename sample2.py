parent_scope = dict(
    {
        "IoC.Scope.Parent": None,
        "IoC.Scope.Create.Empty": {},
        "IoC.Scope.Create": None,
        "IoC.Scope.Current": lambda: parent_scope,
    }
)
current_scope = dict({"IoC.Scope.Parent": parent_scope})

parent_scope["x"] = 10
parent_scope["y"] = 20
current_scope["z"] = 30


# print(json.dumps(parent_scope, indent=4))
# print(json.dumps(current_scope, indent=4))
# print(parent_scope)
# print(current_scope)
print(parent_scope["IoC.Scope.Current"]())
