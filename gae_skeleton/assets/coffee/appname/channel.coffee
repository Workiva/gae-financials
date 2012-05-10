

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

    #sendMessage: (message) =>
        #console.log(message)

    onopen: =>
        console.log('open')

    onmessage: =>
        console.log('message')

    onerror: =>
        console.log('error')

    onclose: =>
        console.log('close')


