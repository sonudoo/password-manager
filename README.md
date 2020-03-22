### Password Manager

This is a simple flask application that creates APIs that can be used to manage your secrets (like password, pin, keys, etc.). The APIs can be preferably accessed using cURL. There are 3 operations that are supported:

* __Insert__: To insert new secrets.
* __Query__: To query the secrets. Two subtypes of query operations are supported:
    - <em>Type 1</em>: To search for secrets by domain (and username).
    - <em>Type 2</em>: To decrypt and get secrets of a single record.
* __Update__: To update the username and secrets of a given record.

#### Build status

|        Pipeline        |          Status          |
|------------------------|--------------------------|
|   Build, Lint & Test   | [![Actions Status](https://github.com/sonudoo/password-manager/workflows/Python%20application/badge.svg)](https://github.com/sonudoo/password-manager/actions) |


#### Setup

- There are 3 MongoDB collections that are required to setup the application:

    1. __Auth collection__: This collection contains hashed authentication keys that the client send via __auth-key__ header to authenticate the application. This collection must be manually created.

        | Field |         Description                    |
        |-------|----------------------------------------|
        | key   | Stores the authentication key as hash. | 

    2. __Master collection__: This collection contains hashed master password and master key that are used for generation of cipher keys that are inturn used to encrypt all the secrets. The cipher keys are generated using an algorithm mentioned in the following section. This cipher key is used as the key and initialization vector of AES cipher (CBC mode). The AES cipher is then used for encrypting all the secrets before storing it in the password manager collection. The secrets are also decrypted using the same AES cipher. This collection must be manually created. This collection must contain only a single record with the following fields.

        |       Field      |            Description               |
        |------------------|--------------------------------------|
        |  master-password | Stores the master password as  hash. | 
        |  master-key      | Stores the master key as hash.       |

    3. __Password manager collection__: This is the collection where the secrets are stored. This collection is populated and updated via APIs. The combination of domain and username must be unique.

        |   Field  |            Description                     |
        |----------|--------------------------------------------|
        | domain   | Domain (ex. abc.com) for the record.       | 
        | username | Username (ex. xyz@abc.com) for the record. |
        | secrets  | List of secrets stored in encrypted format.|

- Create all the 3 collections in a MongoDB. 
- Add the authentication keys in hashed format to the Auth collection. The hash function must be same as the one in <code>utils/hash.py</code>.
- Add the master password and master key in hashed form (in a single record) to the Master collection. The hash function must be same as the one in <code>utils/hash.py</code>.
- Open <code>constants/database.py</code> and specify all the constants such as mongo URI, satabase name, collection names etc.
- Open <code>constants/key_config.py</code> and specify all key generation constants. Leave it to the default values if unsure.

#### Usage

```diff
- All requests should be made over HTTPS to avoid sniffing of authentication keys, master password and master keys.
```

- Run the flask server:
    ```
    > python app.py
    ```

- Insert new secrets:
    ```
    > curl <url>/insert -H "auth-key: s2v6" -d "master-password=abcd&master-key=1234&domain=abc.com&username=abc@xyz.com&secret=secret1&secret=secret2..."
    ```
    | Parameter       | Type  |         Description                                                                  |
    |-----------------|-------|--------------------------------------------------------------------------------------|
    | auth-key        | Header| Required. Authentication key for application.                                        | 
    | master-password | Body  | Required. Master password for Cipher Key.                                            |
    | master-key      | Body  | Required. Master key for Cipher Key.                                                 |
    | domain          | Body  | Required. Domain (ex. abc.com) for the record.                                       |
    | username        | Body  | Required. Username (ex. abc@xyz.com) for the record.                                 |
    | secret          | Body  | Required. List of secrets for the record. There must be atleast one secret parameter.|

- Query for searching records by domain (and username) (No secret decryption take place in this query):
    ```
    > curl <url>/query -H "auth-key: s2v6" -d "master-password=abcd&master-key=1234&domain=abc.com&username=abc@xyz.com"
    ```
    | Parameter       | Type  |         Description                                                                  |
    |-----------------|-------|--------------------------------------------------------------------------------------|
    | auth-key        | Header| Required. Authentication key for application.                                        |
    | query-type      | Body  | Required. The value must be set to 1.                                                | 
    | master-password | Body  | Required. Master password for Cipher Key.                                            |
    | master-key      | Body  | Required. Master key for Cipher Key.                                                 |
    | domain          | Body  | Required. Domain (ex. abc.com) for the record.                                       |
    | username        | Body  | Optional. Username (ex. abc@xyz.com) for the record.                                 |



- Query for decrypting secrets for a single record:
    ```
    > curl <url>/query -H "auth-key: s2v6" -d "query-type=1&master-password=abcd&master-key=1234&domain=abc.com&username=abc@xyz.com"
    ```
    | Parameter       | Type  |         Description                                                                  |
    |-----------------|-------|--------------------------------------------------------------------------------------|
    | auth-key        | Header| Required. Authentication key for application.                                        | 
    | query-type      | Body  | Required. The value must be set to 2.                                                | 
    | master-password | Body  | Required. Master password for Cipher Key.                                            |
    | master-key      | Body  | Required. Master key for Cipher Key.                                                 |
    | domain          | Body  | Required. Domain (ex. abc.com) for the record.                                       |
    | username        | Body  | Required if multiple matches are found. Username (ex. abc@xyz.com) for the record.   |

- Update for decrypting secrets for a single record:
    ```
    > curl <url>/update -H "auth-key: s2v6" -d "master-password=abcd&master-key=1234&domain=abc.com&username=abc@xyz.com&new-username=cba@xyz.com&new-secret=secret1&new-secret=secret2..."
    ```
    | Parameter       | Type  |         Description                                                                      |
    |-----------------|-------|------------------------------------------------------------------------------------------|
    | auth-key        | Header| Required. Authentication key for application.                                            | 
    | master-password | Body  | Required. Master password for Cipher Key.                                                |
    | master-key      | Body  | Required. Master key for Cipher Key.                                                     |
    | domain          | Body  | Required. Domain (ex. abc.com) for the record.                                           |
    | username        | Body  | Required if multiple matches are found. Username (ex. abc@xyz.com) for the record.       |
    | new-username    | Body  | Optional. New Username (ex. cba@xyz.com) for the record.                                 |
    | new-secret      | Body  | Optional. List of new secrets for the record. They will REPLACE all the existing secrets.|

#### Cryptography

__Cipher Key Generation Algorithm__

The constants are defined in <code>constants/key_config.py</code>. The key generated by the following algorithm is used as the key and initialization vector for AES cipher (CBC mode).

1. The delta for caesar cipher is computed as the mod inverse of master key under self.MOD.
2. The randomizer is seeded with the master key.
3. The key is initialized to the master password.
3. The key is trimmed (if length is greater than CIHER_KEY_LENGTH) or padded (by repeatation, if length is less than CIHER_KEY_LENGTH).
4. For CIPHER_KEY_CHURN_COUNT number of times:

    a. Caesar cipher is applied to the key.
    b. The key is then randomized.
    c. The delta for caesar cipher is re-computed as the mod inverse of existing delta under self.MOD.

__Hash Algorithm__

SHA256 is used for hashing the authentication keys, master password and master key.