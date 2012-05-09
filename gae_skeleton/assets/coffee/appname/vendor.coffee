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


class App.Appname.Views.VendorApp extends App.Appname.Views.App
    template: JST['vendor/view']
    addView: null
    listView: null

    render: =>
        @$el.html(@template())

        @listView = new App.Appname.Views.ListApp(
            'VendorList', @$("#vendorlist"))
        @addView = new App.Appname.Views.AddApp(
            App.Appname.Models.Vendor, App.Appname.Views.VendorEdit)

        @addView.on("addItem", @addVendor, this)

        $("#add_new").focus()
        return this

    addVendor: (model) =>
        @listView.addOne(model)

    onClose: =>
        @addView.close()
        @listView.close()


class App.Appname.Views.VendorList extends Backbone.View
    template: JST['vendor/list']
    tagName: "tr"
    editView: null

    events:
        "click .edit-button": "edit"
        "click .remove-button": "clear"

    initialize: =>
        @model.bind('change', @render, this)
        @model.bind('destroy', @remove, this)

    render: =>
        @$el.html(@template(@model.toJSON()))
        return this

    edit: =>
        @editView = new App.Appname.Views.VendorEdit({model: @model})
        @editView.on("save", @save, this)
        el = @editView.render(true).$el
        el.modal('show')
        el.find('input.code').focus()

    save: (model) =>
        @editView.$el.modal('hide')
        @editView.close()

    clear: =>
        @model.clear()


class App.Appname.Views.VendorEdit extends Backbone.View
    template: JST['vendor/edit']
    tagName: "div"

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

    clear: =>
        @model.clear()

    save: =>
        @model.tags.each((tag) ->
            tag.edit_view.close()
        )
        @model.save(
            name: @$('input.name').val()
            notes: $.trim(@$('textarea.notes').val())
        )
        @trigger('save', @model)

    addTag: () =>
        newModel = new @model.tags.model()
        @model.tags.add(newModel)

        editView = new App.Appname.Views.TagEdit({model: newModel})
        @$el.find('fieldset.tags').append(editView.render().el)

    updateOnEnter: (e) =>
        if e.keyCode == 13
            @save()

