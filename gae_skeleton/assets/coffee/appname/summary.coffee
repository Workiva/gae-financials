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


class App.Appname.Models.Summary extends Backbone.Model
    idAttribute: 'key'
    urlRoot: '/service/summary'
    defaults: ->
        return {
            key: "",
            tag: "",
            period: "",
            period_type: "",
            stats:
                n: ""
                s: ""
        }

    validate: (attrs) =>
        hasError = false
        errors = {}

        if _.isEmpty(attrs.tag)
            hasError = true
            errors.date = "Missing tag."

        if _.isEmpty(attrs.period)
            hasError = true
            errors.vendor = "Missing period."

        if hasError
            return errors



class App.Appname.Views.SummaryChannelHandlers extends App.Appname.Views.ChannelHandlers

    constructor: (@collection, @periodType) ->
        App.Appname.Events.bind("period:change", @setPeriodType)

    setCollection: (collection) =>
        @collection = collection

    setPeriodType: (periodType) =>
        @periodType = periodType

    startsWith: (str, starts) ->
        str = '' + str
        starts = '' + starts
        return str.length >= starts.length and str.substr(0, starts.length) == starts

    onmessage: (messages) =>
        messages = JSON.parse(messages.data)
        to_add = []
        for message in messages.messages
            if not @startsWith(message.what, 'Summaries')
                continue

            for summary in message.summaries
                if summary.period_type != @periodType
                    continue

                model = @collection.get(summary.key)
                if model
                    model.set(summary)
                else
                    to_add.push(summary)

        if to_add.length
            @collection.add(to_add)


class App.Appname.Collections.SummaryList extends Backbone.Collection
    url: '/service/summary'
    model: App.Appname.Models.Summary

    initialize: ->
        handler = new App.Appname.Views.SummaryChannelHandlers()
        handler.setCollection(this)
        handler.setPeriodType(this)
        channelapp = new App.Appname.Views.ChannelApp()
        channelapp.setupChannel(handler)


class App.Appname.Views.SummaryApp extends App.Appname.Views.ModelApp
    template: JST['summary/view']
    modelType: App.Appname.Models.Summary

    events:
        "change #period_type": "updatePeriodType"

    updatePeriodType: ->
        period_type = @$("#period_type").val()
        App.Appname.Events.trigger("period:change", period_type, this)
        @listView.collection.each((model) ->
            model.trigger('destroy')
        )
        @listView.collection.fetch({data: {period: period_type}})


class App.Appname.Views.SummaryList extends App.Appname.Views.ListView
    template: JST['summary/list']
    modelType: App.Appname.Models.Summary

