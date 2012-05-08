
Backbone.Model::nestCollection = (attributeName, nestedCollection) ->
    @attributes[attributeName] = (model.attributes for model in nestedCollection.models)

    # create empty arrays if none
    nestedCollection.bind('add', (initiative) =>
        if !@get(attributeName)
            @attributes[attributeName] = []
        @get(attributeName).push(initiative.attributes)
    )

    nestedCollection.bind('remove', (initiative) =>
        updateObj = {}
        updateObj[attributeName] = _.without(@get(attributeName), initiative.attributes)
        @set(updateObj)
    )

    return nestedCollection

