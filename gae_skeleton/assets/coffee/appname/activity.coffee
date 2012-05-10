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


class App.Appname.Models.Activity extends Backbone.Model

    defaults: ->
        return {
            location: "",
            time: "",
            what: ""
        }


class App.Appname.Collections.ActivityList extends Backbone.Collection
    model: App.Appname.Models.Activity


class App.Appname.Views.ActivityApp extends App.Appname.Views.App

    render: =>
        @$el.html('activity')

        channelapp = new App.Appname.Views.ChannelApp()
        channelapp.setupChannel()

        return this


class App.Appname.Views.ChannelApp extends Backbone.View
    channelId: null
    socket: null
    timeoutAction: null

    setupChannel: =>
        handler = new App.Appname.Views.ChannelHandlers()

        $.ajax '/service/channel/token'
            type: 'GET'
            dataType: 'json'
            error: (jqXHR, textStatus, errorThrown) =>
                console.log(textStatus)
                console.log(errorThrown)
            success: (data, status, jqXHR) =>
                channel = new goog.appengine.Channel(data.token)
                @socket = channel.open(handler)


class App.Appname.Views.ChannelHandlers

    sendMessage: (message) =>
        console.log(message)
        
    onopen: =>
        console.log('open')

    onmessage: =>
        console.log('message')

    onerror: =>
        console.log('error')

    onclose: =>
        console.log('close')


