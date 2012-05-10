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


class App.Appname.Collections.TransactionList extends Backbone.Collection
    url: '/service/transaction'
    model: App.Appname.Models.Transaction


class App.Appname.Views.TransactionEdit extends App.Appname.Views.EditView
    template: JST['transaction/edit']
    modelType: App.Appname.Models.Transaction

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

        return super(as_modal)

    save: =>
        @model.save(
            date: @$('input.date').val()
            vendor: @$('input.vendor').val()
            amount: @$('input.amount').val()
        )

        super()


class App.Appname.Views.TransactionApp extends App.Appname.Views.ModelApp
    template: JST['transaction/view']
    modelType: App.Appname.Models.Transaction
    form: App.Appname.Views.TransactionEdit


class App.Appname.Views.TransactionList extends App.Appname.Views.ListView
    template: JST['transaction/list']
    modelType: App.Appname.Models.Transaction

