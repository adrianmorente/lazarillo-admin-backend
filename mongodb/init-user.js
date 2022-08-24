// Create database
db = db.getSiblingDB('lazarillo');

// Create collection where devices are stored
db.createCollection('devices');

// Add user that lazarillo_flask_backend authenticates to
db.createUser({
    user: 'mongouser',
    pwd: 'mongo_password',
    roles: [{
        role: 'readWrite',
        db: 'lazarillo'
    }]
});
