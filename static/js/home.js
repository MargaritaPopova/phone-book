// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/phones',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(phone) {
            let ajax_options = {
                type: 'POST',
                url: 'api/phones',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(phone)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(phone) {
            let ajax_options = {
                type: 'PUT',
                url: `api/phones/${phone.phone_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'text',
                data: JSON.stringify(phone)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
                console.log('successful update');
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                console.log('update failed');
            })
        },
        'delete': function(phone_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `api/phones/${phone_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $phone_id = $('#phone_id'),
        $first_name = $('#first_name'),
        $last_name = $('#last_name'),
        $number = $('#number');

    // return the API
    return {
        reset: function() {
            $phone_id.val('')
            $first_name.val('').focus();
            $last_name.val('');
            $number.val('');
        },
        update_editor: function(phone) {
            $phone_id.val(phone.phone_id);
            $first_name.val(phone.first_name).focus();
            $last_name.val(phone.last_name);
            $number.val(phone.number);
        },
        build_table: function(phones) {
            let rows = ''

            // clear the table
            $('.phones table > tbody').empty();

            // did we get a phones array?
            if (phones) {
                for (let i=0, l=phones.length; i < l; i++) {
                    rows += `<tr data-phone-id="${phones[i].phone_id}">
                    <td class="first_name">${phones[i].first_name}</td>
                    <td class="last_name">${phones[i].last_name}</td>
                    <td class="number">${phones[i].number}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $phone_id = $('#phone_id'),
        $first_name = $('#first_name'),
        $last_name = $('#last_name'),
        $number = $('#number');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(first_name, last_name, number) {
        return first_name !== "" && last_name !== "" && number !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let first_name = $first_name.val(),
            last_name = $last_name.val(),
            number = $number.val();

        e.preventDefault();

        if (validate(first_name, last_name, number)) {
            model.create({
                first_name: first_name,
                last_name: last_name,
                number: number
            })
        } else {
            alert('Problem with name or number input');
        }
    });

    $('#update').click(function(e) {
        let phone_id = $phone_id.val(),
            first_name = $first_name.val(),
            last_name = $last_name.val(),
            number = $number.val();

        e.preventDefault();

        if (validate(first_name, last_name)) {
            model.update({
                phone_id: phone_id,
                first_name: first_name,
                last_name: last_name,
            })
        } else {
            alert('Problem with name or number input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let phone_id = $phone_id.val();

        e.preventDefault();

        if (validate('placeholder', phone_id)) {
            model.delete(phone_id)
        } else {
            alert('Problem with number input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            phone_id,
            first_name,
            last_name,
            number;

        phone_id = $target
            .parent()
            .attr('data-phone-id');

        first_name = $target
            .parent()
            .find('td.first_name')
            .text();

        last_name = $target
            .parent()
            .find('td.last_name')
            .text();

        number = $target
            .parent()
            .find('td.number')
            .text();

        view.update_editor({
            phone_id: phone_id,
            first_name: first_name,
            last_name: last_name,
            number: number
        });
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        alert('there\'s an error in field data: ' + errorThrown)
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));