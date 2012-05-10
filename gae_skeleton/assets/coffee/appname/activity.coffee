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
        #@$el.css('height', '500px')

        #map = new L.Map(@el)

        #api_key = ''

        #cloud = new L.TileLayer(
            #'http://{s}.tile.cloudmade.com/' + api_key + '/997/256/{z}/{x}/{y}.png',
            #{
                #attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
                #maxZoom: 18
            #})
        #map.setView(new L.LatLng(51.505, -0.09), 13)
            #.addLayer(cloud)

        #channelapp = new App.Appname.Views.ChannelApp()
        #channelapp.setupChannel()

        return this

    #onClose: =>
        #@$el.html('')
        #chanelapp.

