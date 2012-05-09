#
# Copyright 2012 Ezox Systems LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


class App.Appname.Models.Tag extends Backbone.Model
    defaults: ->
        return {
            name: ""
        }

    validate: (attrs) =>
        hasError = false
        errors = {}

        if _.isEmpty(attrs.name)
            hasError = true
            errors.name = "Missing name."

        if hasError
            return errors

    clear: ->
        this.destroy()


class App.Appname.Collections.Tags extends Backbone.Collection
    model: App.Appname.Models.Tag


class App.Appname.Views.Tag extends Backbone.View
    tagName: "div"
    className: "tag-view"
    template: JST['tag/view']

    initialize: ->
        @model.bind('change', @render, this)
        @model.bind('destroy', @remove, this)
        @model.view = this

    render: =>
        @$el.html(@template(@model.toJSON()))
        return this

    clear: =>
        @model.clear()


class App.Appname.Views.TagEdit extends Backbone.View
    tagName: "fieldset"
    className: "tag-edit"
    template: JST['tag/edit']

    events:
        "click a.remove": "clear"

    initialize: ->
        @model.bind('change', @render, this)
        @model.bind('destroy', @remove, this)
        @model.edit_view = this

    render: =>
        @$el.html(@template(@model.toJSON()))
        return this

    close: =>
        @model.set(
            name: @$('input.name').val()
        )
        return this

    clear: =>
        @model.clear()

