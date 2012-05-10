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
    template: JST['activity/view']

    render: =>
        @$el.html(@template())

        return this

#class App.Appname.Views.ActivityApp extends App.Appname.Views.App
    #template: JST['activity/view']
    #map: null
    #cloud: null

    #initialize: =>
        #@cloud = new L.TileLayer(
            #'http://{s}.tile.cloudmade.com/' + CLOUD_API_KEY + '/997/256/{z}/{x}/{y}.png',
            #{
                #attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
                #maxZoom: 18
            #})

    #render: =>
        #@$el.html(@template())
        #@map = new L.Map(this.$("#map").get(0))

        #@map.setView(new L.LatLng('51.505', '-0.09'), 13, forceReset=true)
            #.addLayer(@cloud)
            #.invalidateSize()

        ##channelapp = new App.Appname.Views.ChannelApp()
        ##channelapp.setupChannel()

        #return this

    #close: =>
        #this.$("#map").html('')
        #@map.removeLayer(@cloud)
        #@map = null
        #@cloud = null
        #console.log('close')

    ##close: =>
        ##@$el.unbind()
        ##@$el.empty()
        ##console.log('close')
