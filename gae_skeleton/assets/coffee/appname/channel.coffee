

class App.Appname.Views.ChannelApp extends Backbone.View
    channelId: null
    socket: null
    timeoutAction: null

    setupChannel: (handler) =>
        if not handler
            return

        $.ajax('/service/channel/token'
            type: 'GET'
            dataType: 'json'
            error: (jqXHR, textStatus, errorThrown) =>
                console.log(textStatus)
                console.log(errorThrown)
            success: (data, status, jqXHR) =>
                console.log(data.token)
                channel = new goog.appengine.Channel(data.token)
                @socket = channel.open(handler)
                window.S = @socket
        )


class App.Appname.Views.ChannelHandlers

    onopen: =>
        console.log('open')

    onmessage: (message) =>
        console.log('message')
        console.log(message)

    onerror: (error) =>
        console.log('error')
        console.log(error)

    onclose: =>
        console.log('close')


