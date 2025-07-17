// MongoDB initialization script for Genesis Backend
// Creates necessary users, databases, and collections

// Switch to genesis database
db = db.getSiblingDB('genesis_db');

// Create genesis user with read/write permissions
db.createUser({
  user: 'genesis',
  pwd: 'genesis',
  roles: [
    {
      role: 'readWrite',
      db: 'genesis_db'
    }
  ]
});

// Create collections with validation schemas
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['email', 'createdAt'],
      properties: {
        _id: {
          bsonType: 'objectId'
        },
        email: {
          bsonType: 'string',
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
          description: 'must be a valid email address'
        },
        name: {
          bsonType: 'string',
          maxLength: 100,
          description: 'must be a string and is optional'
        },
        password: {
          bsonType: 'string',
          description: 'hashed password'
        },
        isActive: {
          bsonType: 'bool',
          description: 'user active status'
        },
        roles: {
          bsonType: 'array',
          items: {
            bsonType: 'string'
          },
          description: 'user roles array'
        },
        profile: {
          bsonType: 'object',
          properties: {
            firstName: { bsonType: 'string' },
            lastName: { bsonType: 'string' },
            avatar: { bsonType: 'string' },
            bio: { bsonType: 'string' }
          }
        },
        createdAt: {
          bsonType: 'date',
          description: 'creation timestamp is required'
        },
        updatedAt: {
          bsonType: 'date',
          description: 'last update timestamp'
        }
      }
    }
  }
});

// Create indexes for users collection
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ 'profile.firstName': 1, 'profile.lastName': 1 });
db.users.createIndex({ roles: 1 });
db.users.createIndex({ createdAt: 1 });
db.users.createIndex({ isActive: 1 });

// Create products collection
db.createCollection('products', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'price', 'createdAt'],
      properties: {
        _id: {
          bsonType: 'objectId'
        },
        name: {
          bsonType: 'string',
          maxLength: 200,
          description: 'product name is required'
        },
        description: {
          bsonType: 'string',
          description: 'product description'
        },
        price: {
          bsonType: 'number',
          minimum: 0,
          description: 'price must be a positive number'
        },
        category: {
          bsonType: 'string',
          description: 'product category'
        },
        tags: {
          bsonType: 'array',
          items: {
            bsonType: 'string'
          }
        },
        stock: {
          bsonType: 'int',
          minimum: 0,
          description: 'stock quantity'
        },
        isActive: {
          bsonType: 'bool'
        },
        images: {
          bsonType: 'array',
          items: {
            bsonType: 'string'
          }
        },
        specifications: {
          bsonType: 'object'
        },
        createdAt: {
          bsonType: 'date'
        },
        updatedAt: {
          bsonType: 'date'
        }
      }
    }
  }
});

// Create indexes for products collection
db.products.createIndex({ name: 'text', description: 'text' });
db.products.createIndex({ category: 1 });
db.products.createIndex({ tags: 1 });
db.products.createIndex({ price: 1 });
db.products.createIndex({ isActive: 1 });
db.products.createIndex({ createdAt: 1 });

// Create orders collection
db.createCollection('orders', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['userId', 'items', 'totalAmount', 'createdAt'],
      properties: {
        _id: {
          bsonType: 'objectId'
        },
        userId: {
          bsonType: 'objectId',
          description: 'reference to user'
        },
        items: {
          bsonType: 'array',
          minItems: 1,
          items: {
            bsonType: 'object',
            required: ['productId', 'quantity', 'price'],
            properties: {
              productId: { bsonType: 'objectId' },
              quantity: { bsonType: 'int', minimum: 1 },
              price: { bsonType: 'number', minimum: 0 },
              name: { bsonType: 'string' }
            }
          }
        },
        totalAmount: {
          bsonType: 'number',
          minimum: 0
        },
        status: {
          bsonType: 'string',
          enum: ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        },
        shippingAddress: {
          bsonType: 'object',
          properties: {
            street: { bsonType: 'string' },
            city: { bsonType: 'string' },
            state: { bsonType: 'string' },
            zipCode: { bsonType: 'string' },
            country: { bsonType: 'string' }
          }
        },
        paymentMethod: {
          bsonType: 'string',
          enum: ['credit_card', 'debit_card', 'paypal', 'stripe', 'cash']
        },
        createdAt: {
          bsonType: 'date'
        },
        updatedAt: {
          bsonType: 'date'
        }
      }
    }
  }
});

// Create indexes for orders collection
db.orders.createIndex({ userId: 1 });
db.orders.createIndex({ status: 1 });
db.orders.createIndex({ 'items.productId': 1 });
db.orders.createIndex({ createdAt: 1 });
db.orders.createIndex({ totalAmount: 1 });

// Insert sample data for development
db.users.insertMany([
  {
    email: 'admin@genesis.dev',
    name: 'Genesis Admin',
    password: '$2b$12$hashed_password_here',
    isActive: true,
    roles: ['admin', 'user'],
    profile: {
      firstName: 'Genesis',
      lastName: 'Admin',
      bio: 'System administrator'
    },
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    email: 'user@genesis.dev',
    name: 'Test User',
    password: '$2b$12$hashed_password_here',
    isActive: true,
    roles: ['user'],
    profile: {
      firstName: 'Test',
      lastName: 'User',
      bio: 'Regular user for testing'
    },
    createdAt: new Date(),
    updatedAt: new Date()
  }
]);

db.products.insertMany([
  {
    name: 'Sample Product 1',
    description: 'This is a sample product for testing',
    price: 29.99,
    category: 'electronics',
    tags: ['sample', 'test', 'electronics'],
    stock: 100,
    isActive: true,
    images: ['https://example.com/image1.jpg'],
    specifications: {
      weight: '1kg',
      dimensions: '10x10x5cm',
      color: 'black'
    },
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    name: 'Sample Product 2',
    description: 'Another sample product for testing',
    price: 49.99,
    category: 'clothing',
    tags: ['sample', 'test', 'clothing'],
    stock: 50,
    isActive: true,
    images: ['https://example.com/image2.jpg'],
    specifications: {
      size: 'M',
      material: 'cotton',
      color: 'blue'
    },
    createdAt: new Date(),
    updatedAt: new Date()
  }
]);

// Create test database
db = db.getSiblingDB('genesis_test_db');

// Create test user
db.createUser({
  user: 'genesis_test',
  pwd: 'genesis_test',
  roles: [
    {
      role: 'readWrite',
      db: 'genesis_test_db'
    }
  ]
});

// Create same collections in test database (without sample data)
db.createCollection('users');
db.createCollection('products');
db.createCollection('orders');

// Create indexes in test database
db.users.createIndex({ email: 1 }, { unique: true });
db.products.createIndex({ name: 'text', description: 'text' });
db.orders.createIndex({ userId: 1 });

print('Genesis Backend MongoDB initialization completed successfully');
