###
Copyright 2012 Ezox Systems LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
###

Backbone.View.prototype.close = (() ->
    this.remove()
    this.unbind()
    this.trigger('closing')
    this.off()
    if this.onClose
        this.onClose()
)

extend = (obj, mixin) ->
    obj[name] = method for name, method of mixin
    return obj

include = (klass, mixin) ->
    extend klass.prototype, mixin

window.App = (() ->
    module: (() ->
        # Internal module cache.
        modules = {}

        # Create a new module reference scaffold or load an
        # existing module.
        return (name) ->
            # If this module has already been created, return it.
            if (modules[name])
                return modules[name]

            # Create a module and save it under this name
            return modules[name] = {
                Models: {}
                Collections: {}
                Views: {}
            }
    )()
)()

