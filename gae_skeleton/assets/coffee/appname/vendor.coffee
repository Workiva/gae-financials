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


class App.Appname.Models.Vendor extends Backbone.Model
    idAttribute: 'key'
    urlRoot: '/service/vendor'
    defaults: ->
        return {
            key: "",
            name: "",
            tags: [],
            notes: "",
        }

    initialize: () ->
        @tags = @nestCollection(
            'tags',
            new App.Appname.Collections.Tags(@get('tags')))

    validate: (attrs) =>
        hasError = false
        errors = {}

        if _.isEmpty(attrs.name)
            hasError = true
            errors.name = "Missing name."

        if hasError
            return errors

    clear: =>
        @destroy()


class App.Appname.Collections.VendorList extends Backbone.Collection
    url: '/service/vendor'
    model: App.Appname.Models.Vendor


class App.Appname.Views.VendorEdit extends App.Appname.Views.EditView
    template: JST['vendor/edit']
    modelType: App.Appname.Models.Vendor

    events:
        "click a.destroy": "clear"
        "click a.add_tag": "addTag"
        "keypress .edit": "updateOnEnter"
        "click .remove-button": "clear"
        "hidden": "close"

    render: (as_modal) =>
        el = @$el
        el.html(@template(@model.toJSON()))
        @model.tags.each((info, i) ->
            editView = new App.Appname.Views.TagEdit({model: info})
            el.find('fieldset.tags').append(editView.render().el)
        )
        if as_modal
            el.attr('class', 'modal')
        return this

    save: =>
        @model.tags.each((tag) ->
            tag.edit_view.close()
        )
        @model.save(
            name: @$('input.name').val()
            notes: $.trim(@$('textarea.notes').val())
        )

        super()

    addTag: () =>
        newModel = new @model.tags.model()
        @model.tags.add(newModel)

        editView = new App.Appname.Views.TagEdit({model: newModel})
        @$el.find('fieldset.tags').append(editView.render().el)


class App.Appname.Views.VendorApp extends App.Appname.Views.ModelApp
    template: JST['vendor/view']
    modelType: App.Appname.Models.Vendor
    form: App.Appname.Views.VendorEdit


class App.Appname.Views.VendorList extends App.Appname.Views.ListView
    template: JST['vendor/list']
    modelType: App.Appname.Models.Vendor

