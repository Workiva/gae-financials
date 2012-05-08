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


class App.Appname.Views.AddApp extends App.Appname.Views.App
    modelType: null
    addForm: null
    view: null

    events:
        "click .add-button": "add"

    initialize: (modelType, form) =>
        @modelType = modelType
        @addForm = form

    add: =>
        if @view
            @addClose()
        else
            @addOpen()

    addOpen: =>
        @model = new @modelType()
        @view = new @addForm({model: @model})
        @view.on("save", this.save, this)
        el = @view.render().el
        $("#add_area").html(el)
            .find('input.code').focus()
        $("#add_new").text('Search Mode')

    addClose: =>
        @view.onClose = null
        @view.close()
        @view = null
        this.$("#add_new").text('Add Mode')
                          .focus()

    save: (model) =>
        valid = @view.model.isValid()
        if valid
            this.trigger('addItem', model)
            @view = null
            @add()

    onClose: =>
        if @view
            @view.close()


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

