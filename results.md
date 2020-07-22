# Intent Cross-Validation Results (5 folds)
|          class          |support|f1-score|             confused_with             |
|-------------------------|------:|-------:|---------------------------------------|
|macro avg                |    253|  0.8023|N/A                                    |
|weighted avg             |    253|  0.8019|N/A                                    |
|inform                   |     56|  0.8155|request_vm(4), connect_wifi(4)         |
|get_incident_status      |     18|  0.8500|open_incident(1)                       |
|password_reset           |     15|  0.9677|N/A                                    |
|out_of_scope             |     15|  0.6875|problem_email(2), password_reset(1)    |
|problem_email            |     13|  0.8966|N/A                                    |
|goodbye                  |     13|  0.7500|help(1), confirm(1)                    |
|confirm                  |     13|  0.7586|thank(1), out_of_scope(1)              |
|open_incident            |     12|  0.8800|help(1)                                |
|deny                     |     12|  0.6000|thank(1), confirm(1)                   |
|greet                    |     12|  0.7368|confirm(2), help(1)                    |
|help                     |     11|  0.6667|out_of_scope(1), confirm(1)            |
|connect_wifi             |     11|  0.8462|N/A                                    |
|request_vm               |     10|  0.5263|inform(4), request_biometrics_report(1)|
|create_user              |     10|  0.9474|get_incident_status(1)                 |
|request_biometrics_report|     10|  0.8696|N/A                                    |
|thank                    |      8|  0.8421|N/A                                    |
|bot_challenge            |      8|  0.8000|out_of_scope(2)                        |
|show_menu                |      6|  1.0000|N/A                                    |



# Entity Cross-Validation Results (5 folds)
|    entity    |support|f1-score|precision|recall|
|--------------|------:|--------|---------|------|
|micro avg     |     69|  0.7692|   0.8197|0.7246|
|macro avg     |     69|  0.6927|   0.7587|0.6538|
|weighted avg  |     69|  0.7658|   0.8291|0.7246|
|course_type   |     10|  0.8421|   0.8889|0.8000|
|priority      |     10|  0.8889|        1|0.8000|
|vm_environment|      9|  0.8750|        1|0.7778|
|wifi_network  |      8|  0.9333|        1|0.8750|
|vm_cpu_cores  |      7|  0.5714|   0.5714|0.5714|
|vm_disk_space |      7|  0.6250|   0.5556|0.7143|
|vm_ram        |      6|  0.6154|   0.5714|0.6667|
|ticket_no     |      6|  0.9091|        1|0.8333|
|vm_scalability|      4|  0.6667|        1|0.5000|
|faculty       |      2|N/A     |N/A      |N/A   |
