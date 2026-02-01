# -*- coding: utf-8 -*-
from odoo import http
from odoo import fields
from odoo.http import request, Response
import json

class RideOrderController(http.Controller):

    # create a new ride
    @http.route('/yaawi/api/v1/ride', auth='public', type='http', methods=['POST'], csrf=False)
    def create(self, passenger_id=None, driver_id=None, ride_type=None, pickup_lat=None, pickup_lon=None, destination_lat=None, destination_lon=None, start_time=None, seats_available=1, **kwargs):
        """Créer une nouvelle course avec calcul automatique du prix"""

        required_fields = ['passenger_id', 'ride_type', 'pickup_lat', 'pickup_lon', 'destination_lat', 'destination_lon']
        data = request.get_json_data()

        # Vérifier les champs obligatoires
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response(json.dumps({
                'error': f"Les champs suivants sont obligatoires : {', '.join(missing_fields)}"
            }), content_type='application/json', status=400)
        
        # Créer la course
        ride = request.env['ride.order'].sudo().create({
            'passenger_id': data.get('passenger_id'),
            'driver_id': data.get('driver_id'),
            'ride_type': data.get('ride_type'),
            'pickup_lat': data.get('pickup_lat'),
            'pickup_lon': data.get('pickup_lon'),
            'destination_lat': data.get('destination_lat'),
            'destination_lon': data.get('destination_lon'),
            'start_time': data.get('start_time') or fields.Datetime.now(),
            'seats_available': data.get('seats_available', 1),
        })

        return Response(json.dumps({
            'success': True,
            'message': 'Course créée avec succès',
            'ride_id': ride.id,
            'ride_price': ride.price,
            'payment_status': ride.payment_status,
            'status': ride.status,
            'distance_km': round(ride._haversine_distance(
                ride.pickup_lat, ride.pickup_lon, ride.destination_lat, ride.destination_lon), 2)
        }), content_type='application/json', status=201)
    
    # update ride
    @http.route('/yaawi/api/v1/ride/<int:ride_id>', auth='public', type='http', methods=['PUT'], csrf=False)
    def update(self, ride_id, **kwargs):
        """Mettre à jour les informations d'une course"""

        ride = request.env['ride.order'].sudo().browse(ride_id)

        if not ride:
            return Response(json.dumps({
                'error': 'Course introuvable'
            }), content_type='application/json', status=404)

        data = request.get_json_data()

        ride.write(data)

        return Response(json.dumps({
            'success': True,
            'message': 'Course mise à jour avec succès'
        }), content_type='application/json', status=200)

    # get ride by id
    @http.route('/yaawi/api/v1/ride/<int:ride_id>', auth='public', type='http', methods=['GET'], csrf=False)
    def get(self, ride_id):
        """Récupérer les informations d'une course"""

        ride = request.env['ride.order'].sudo().browse(ride_id)

        if not ride:
            return Response(json.dumps({
                'error': 'Course introuvable'
            }), content_type='application/json', status=404)

        return Response(json.dumps({
            'success': True,
            'ride_id': ride.id,
            'passenger_id': ride.passenger_id.id,
            'driver_id': ride.driver_id.id,
            'ride_type': ride.ride_type,
            'pickup_lat': ride.pickup_lat,
            'pickup_lon': ride.pickup_lon,
            'destination_lat': ride.destination_lat,
            'destination_lon': ride.destination_lon,
            'start_time': ride.start_time.isoformat() if ride.start_time else None,
            'seats_available': ride.seats_available,
            'price': ride.price,
            'payment_status': ride.payment_status,
            'status': ride.status,
            'distance' : ride.distance
        }), content_type='application/json', status=200)


    # get all rides
    @http.route('/yaawi/api/v1/rides', auth='public', type='http', methods=['GET'], csrf=False)
    def list(self):
        """Lister toutes les courses"""

        rides = request.env['ride.order'].sudo().search_read([])

        return Response(json.dumps({
            'success': True,
            'rides': [{
                'ride_id': ride.id,
                'passenger_id': ride.passenger_id.id,
                'driver_id': ride.driver_id.id,
                'ride_type': ride.ride_type,
                'pickup_lat': ride.pickup_lat,
                'pickup_lon': ride.pickup_lon,
                'destination_lat': ride.destination_lat,
                'destination_lon': ride.destination_lon,
                'start_time': ride.start_time.isoformat() if ride.start_time else None,
                'seats_available': ride.seats_available,
                'price': ride.price,
                'payment_status': ride.payment_status,
                'status': ride.status,
                'distance' : ride.distance
            } for ride in rides]
        }), content_type='application/json', status=200)

    # get passenger rides
    @http.route('/yaawi/api/v1/passenger/<int:passenger_id>/rides', auth='public', type='http', methods=['GET'], csrf=False)
    def get_passenger_rides(self, passenger_id):
        """Lister toutes les courses d'un passager"""

        rides = request.env['ride.order'].sudo().search_read([('passenger_id', '=', passenger_id)])

        return Response(json.dumps({
            'success': True,
            'rides': [{
                'ride_id': ride.id,
                'passenger_id': ride.passenger_id.id,
                'driver_id': ride.driver_id.id,
                'ride_type': ride.ride_type,
                'pickup_lat': ride.pickup_lat,
                'pickup_lon': ride.pickup_lon,
                'destination_lat': ride.destination_lat,
                'destination_lon': ride.destination_lon,
                'start_time': ride.start_time.isoformat() if ride.start_time else None,
                'seats_available': ride.seats_available,
                'price': ride.price,
                'payment_status': ride.payment_status,
                'status': ride.status,
                'distance' : ride.distance
            } for ride in rides]
        }), content_type='application/json', status=200)
        
    # get rides by driver
    @http.route('/yaawi/api/v1/driver/<int:driver_id>/rides', auth='public', type='http', methods=['GET'], csrf=False)
    def get_driver_rides(self, driver_id):
        """Lister toutes les courses d'un conducteur"""

        rides = request.env['ride.order'].sudo().search_read([('driver_id', '=', driver_id)])

        return Response(json.dumps({
            'success': True,
            'rides': [{
                'ride_id': ride.id,
                'passenger_id': ride.passenger_id.id,
                'driver_id': ride.driver_id.id,
                'ride_type': ride.ride_type,
                'pickup_lat': ride.pickup_lat,
                'pickup_lon': ride.pickup_lon,
                'destination_lat': ride.destination_lat,
                'destination_lon': ride.destination_lon,
                'start_time': ride.start_time.isoformat() if ride.start_time else None,
                'seats_available': ride.seats_available,
                'price': ride.price,
                'payment_status': ride.payment_status,
                'status': ride.status,
                'distance' : ride.distance
            } for ride in rides]
        }), content_type='application/json', status=200)
        
    # rides by status
    @http.route('/yaawi/api/v1/rides/<string:status>', auth='public', type='http', methods=['GET'], csrf=False)
    def get_rides_by_status(self, status):
        """Lister toutes les courses par statut"""

        rides = request.env['ride.order'].sudo().search_read([('status', '=', status)])

        return Response(json.dumps({
            'success': True,
            'rides': [{
                'ride_id': ride.id,
                'passenger_id': ride.passenger_id.id,
                'driver_id': ride.driver_id.id,
                'ride_type': ride.ride_type,
                'pickup_lat': ride.pickup_lat,
                'pickup_lon': ride.pickup_lon,
                'destination_lat': ride.destination_lat,
                'destination_lon': ride.destination_lon,
                'start_time': ride.start_time.isoformat() if ride.start_time else None,
                'seats_available': ride.seats_available,
                'price': ride.price,
                'payment_status': ride.payment_status,
                'status': ride.status,
                'distance' : ride.distance
            } for ride in rides]
        }), content_type='application/json', status=200)