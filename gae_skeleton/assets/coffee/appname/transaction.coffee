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


class App.Appname.Models.Transaction extends Backbone.Model
    idAttribute: 'key'
    urlRoot: '/service/transaction'
    defaults: ->
        return {
            key: "",
            date: "",
            vendor: "",
            amount: "",
        }

    validate: (attrs) =>
        hasError = false
        errors = {}

        if _.isEmpty(attrs.date)
            hasError = true
            errors.date = "Missing name."
            console.log('no date!')

        if _.isEmpty(attrs.vendor)
            hasError = true
            errors.vendor = "Missing vendor."
            console.log('no vendor!')

        if _.isEmpty(attrs.amount)
            hasError = true
            errors.amount = "Missing amount."
            console.log('no amount!')

        if hasError
            return errors

    clear: =>
        @destroy()


class App.Appname.Collections.TransactionList extends Backbone.Collection
    url: '/service/transaction'
    model: App.Appname.Models.Transaction


class App.Appname.Views.TransactionApp extends App.Appname.Views.App
    template: JST['transaction/view']
    addView: null
    listView: null

    render: =>
        @$el.html(@template())

        @listView = new App.Appname.Views.ListApp(
            'TransactionList', this.$("#transactionlist"))
        @addView = new App.Appname.Views.AddApp(
            App.Appname.Models.Transaction, App.Appname.Views.TransactionEdit)

        @addView.on("addItem", this.addTransaction, this)

        $("#add_new").focus()
        return this

    addTransaction: (model) =>
        @listView.addOne(model)

    onClose: =>
        @addView.close()
        @listView.close()


class App.Appname.Views.TransactionList extends Backbone.View
    template: JST['transaction/list']
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
        @editView = new App.Appname.Views.TransactionEdit({model: @model})
        @editView.on("save", @save, this)
        el = @editView.render(true).$el
        el.modal('show')
        el.find('input.code').focus()

    save: (model) =>
        @editView.$el.modal('hide')
        @editView.close()

    clear: =>
        @model.clear()


class App.Appname.Views.TransactionEdit extends Backbone.View
    template: JST['transaction/edit']
    tagName: "div"

    events:
        "click a.destroy": "clear"
        "keypress .edit": "updateOnEnter"
        "click .remove-button": "clear"
        "hidden": "close"

    render: (as_modal) =>
        el = @$el
        el.html(@template(@model.toJSON()))
        @$el.find('input.vendor').typeahead({
            value_property: 'name'
            updater: (item) =>
                return item.name
            matcher: (item) ->
                return true
            source: (typeahead, query) ->
                $.ajax({
                    type: 'GET'
                    dataType: 'json'
                    url: '/service/vendor'
                    data: {query: query}
                    success: (data) ->
                        typeahead.process(data)
                })
        })
        if as_modal
            el.attr('class', 'modal')
        return this

    clear: =>
        @model.clear()

    save: =>
        console.log(
            date: @$('input.date').val()
            vendor: @$('input.vendor').val()
            amount: @$('input.amount').val()
        )
        @model.save(
            date: @$('input.date').val()
            vendor: @$('input.vendor').val()
            amount: @$('input.amount').val()
        )
        @trigger('save', @model)

    updateOnEnter: (e) =>
        if e.keyCode == 13
            @save()

