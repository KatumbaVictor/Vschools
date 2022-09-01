(async () => {
    try {
        const symbl = new Symbl({
            appId: '6f77634b73416c4c616b575949676d576e494b4a304c44564e446e34644b7551',
            appSecret: '715341643953573431314d65344935496a716a7157566b5078513532445234757a52726a31364a69766f6c4745624430703237525f5637314435356a3774376e',
            reconnectOnError: true
        });
        const connection = await symbl.createConnection();
        connection.connect();
        await connection.startProcessing({
          insightTypes: ["question", "action_item", "follow_up"],
          config: {
            encoding: "OPUS"
          },
          speaker: {
            userId: "user@example.com",
            name: "Your Name Here"
          }
        });
  
        connection.on("message", (speechData) => {
                console.log(speechData[0]);
        });
  
        await Symbl.wait(60000);
        
        await connection.stopProcessing();
        
        connection.disconnect();
    } catch(e) {
        
    }
  
  })();