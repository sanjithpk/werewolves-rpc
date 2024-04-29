syntax = "proto3";

package grpc;

message Empty {}

message Message {
    string name = 1;
    string message = 2;
}

message Name {
    string name = 1;
}

message Credentials {
    string username = 1;
    string password = 2;
}

service ChatServer {
    // This bi-directional stream makes it possible to send and receive Notes between 2 persons
    rpc ChatStream (Name) returns (stream Message);
    rpc HandleMessage (Message) returns (Empty);
    rpc Connect (Credentials) returns (Message);
}