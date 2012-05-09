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

window.App.Appname = App.module('Appname')


class App.Appname.Views.App extends Backbone.View
    el: $("#appnameapp")

    onClose: =>
        @$el.html('')


class App.Appname.Views.ModelApp extends App.Appname.Views.App
    template: null
    modelType: null
    form: null
    addView: null
    editView: null
    listView: null
    searchMode: true

    events:
        "click .add-button": "add"

    render: =>
        @searchMode = true
        App.Appname.Events.bind(@modelType.name + ":add", @addItem, this)
        App.Appname.Events.bind(@modelType.name + ":edit", @editItem, this)

        @$el.html(@template())

        @listView = new App.Appname.Views.ListApp(
            @modelType.name + "List", @$("#" + @modelType.name + "list"))

        $("#add_new").focus()
        return this

    editItem: (model) =>
        @addClose()
        App.Appname.Events.bind(@modelType.name + ":save", this.editSave, this)
        @editView = new @form({model: model})
        el = @editView.render(true).$el
        el.modal('show')
        el.find('input.code').focus()

    addItem: (model) =>
        @listView.addOne(model)
    
    add: =>
        if @searchMode
            @addOpen()
        else
            @addClose()

    addOpen: =>
        @searchMode = false
        App.Appname.Events.bind(@modelType.name + ":save", this.addSave, this)

        @model = new @modelType()
        @addView = new @form({model: @model})

        el = @addView.render().el
        $("#add_area").html(el)
            .find('input.code').focus()

        $("#add_new").text('Search Mode')

    addClose: =>
        App.Appname.Events.unbind(@modelType.name + ":save", this.addSave, this)
        @searchMode = true
        if @addView
            @addView.close()
        @addView = null
        this.$("#add_new").text('Add Mode')
                          .focus()

    addSave: (model) =>
        valid = @addView.model.isValid()
        if valid
            App.Appname.Events.trigger(@modelType.name + ':add', model)
            @addView = null
            @add()

    editSave: (model) =>
        App.Appname.Events.unbind(@modelType.name + ":save", this.editSave, this)
        @editView.$el.modal('hide')
        @editView.close()
        @editView = null

    onClose: =>
        App.Appname.Events.unbind(null, null, this)

        if @addView
            @addView.close()
        if @editView
            @editView.close()


class App.Appname.Views.EditView extends Backbone.View
    tagName: "div"
    modelType: null

    clear: =>
        @model.clear()

    save: =>
        App.Appname.Events.trigger(@modelType.name + ':save', @model, this)

    updateOnEnter: (e) =>
        if e.keyCode == 13
            @save()


class App.Appname.Views.ListView extends Backbone.View
    tagName: "tr"
    modelType: null

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
        App.Appname.Events.trigger(@modelType.name + ":edit", @model, this)

    clear: =>
        @model.clear()


class App.Appname.Views.ListApp extends App.Appname.Views.App

    initialize: (view, el, collection) ->
        if el
            @el = el
        else
            @el = @$el
        if not collection
            collection = view
        @model_view = App.Appname.Views[view]
        @collection = new App.Appname.Collections[collection]
        @collection.bind('add', @addOne, this)
        @collection.bind('reset', @addAll, this)
        @collection.bind('all', @show, this)
        @collection.fetch()

    addOne: (object) =>
        view = new @model_view({model: object})
        object.view = view
        @el.append(view.render().el)

    addAll: =>
        @collection.each(@addOne)

