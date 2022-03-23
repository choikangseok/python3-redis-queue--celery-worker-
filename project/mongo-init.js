db.createUser({
  user: 'my_user',
  pwd: 'my_password',
  roles: [
    {
      role: 'dbOwner',
      db: 'my_database',
    },
  ],
});

db.createCollection('my_collection');

db.my_collection.insertMany([
  {
    First_value: 'test1_first',
    Second_value: 'test1_second',
    Today: 'test1_today'
  },
  {
    First_value: 'test2_first',
    Second_value: 'test2_second',
    Today: 'test2_today'
  }
]);
