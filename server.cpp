//TCP Server

#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>

#define MSG_LEN          100 
#define SESSION_FINISHED 10

using namespace std;

#define error(msg)\
{\
    perror(msg); \
    return (-1); \
}

class ServerSocket {

public:

    char buf[MSG_LEN];
    socklen_t len;
    int sock_desc,temp_sock_desc;
    int yes;
    struct sockaddr_in client, server;

    int Create();
    int Listen(unsigned short int port);
    int Accept();
    int Read();
    void Close();

};


int ServerSocket::Create() {

    sock_desc = socket(AF_INET, SOCK_STREAM, 0);

    if (sock_desc < 0)
      error("Server: ERROR opening socket");

    /* Enable address reuse */
    if (setsockopt(sock_desc, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
        perror("setsockopt");
         exit(1);
     }
     return 0;
}


int ServerSocket::Listen(unsigned short int port) {

    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_port = htons(port);

    printf("Server: RSTREAM:: assigned port number %d\n", ntohs(server.sin_port));



    if (bind(sock_desc, (struct sockaddr*)&server, sizeof(server)) < 0)
        error("Server: ERROR on binding");

    listen(sock_desc, 2);
    len = sizeof(client);

    cout << "Server: Is running .. " << endl;
    return 0;
}


int ServerSocket::Accept()
{
    printf("Server: Accepting new connections.............\n");
    memset(&client, 0, sizeof(client)); // clear the structure sockaddr_in
    temp_sock_desc = accept(sock_desc, (struct sockaddr*) &client, &len); // setup new socket to temp_sock_desc
    if (temp_sock_desc < 0) // if < 0 - means error was occured
    {
        error("Server: ERROR on accept");
	return -1; // return error code
    }

    cout << "Server: Connection accepted ...............\n " << endl;
    return 0;
}


int ServerSocket::Read() {


    char msg[MSG_LEN] = {0,};

    int k = 0;
    while(1)
    {
        k = recv(temp_sock_desc, msg, MSG_LEN, 0/*MSG_NOSIGNAL*/);
        
        
        if (k < 0)
            error("Server: ERROR reading from socket");

        if (k == 0)
        {
            printf("Server: Socket is closed, stop reading.......\n");
            break;
        }

        if (strncmp("exit", msg, 4) == 0)
        {
            printf("Server: Entered 'exit'. Close connection .......... \n");
            return SESSION_FINISHED;               // return session finishing code ( instead of exit(), its a bad practice to use "левую" func to exit )
        }

        if (k > 0)
        {
            msg[k] = '\0'; // in the end of array we should write string terminator '\0'
            printf("Server: Client's message: %s", msg);
            send(temp_sock_desc, msg, k, 0); // MSG_LEN has been here before
    	}

    }

    return 0;
}


void ServerSocket::Close() {

  close(temp_sock_desc);
  close(sock_desc);

}



int main ( int argc, char *argv[] )
{
    if ( argc != 2 ) 
    { // argc should be 2 for correct execution
    // We print argv[0] assuming it is the program name
    fprintf(stderr,"ERROR, no port provided\n");
    cout<<"usage: "<< argv[0] <<" <Server Port>\n";
    return -1; 
    }

    unsigned short int port = atoi(argv[1]);
    
    ServerSocket m_ServerSocket;

    if (m_ServerSocket.Create() != 0)
    	return (-1); // return error code
    if (m_ServerSocket.Listen(port) != 0)
    	return (-1); // return error code

    while (1)
    { 
	if (m_ServerSocket.Accept() == 0) // in other words if (m_ServerSocket.Accept() != 0)  -  means, if socket was not accepted correctly, we ignore it
	   {
    		if (m_ServerSocket.Read() == SESSION_FINISHED) // if return code is SESSION_FINISHED - means, "while" loop should be terminated
            break;
  	     }
    }

    m_ServerSocket.Close(); // destroy the main socket and accepted socket
    return 0; // return success code
}
