# Intent Cross-Validation Results (5 folds)
|          class          |support|f1-score|             confused_with             |
|-------------------------|------:|-------:|---------------------------------------|
|macro avg                |    307|  0.8985|N/A                                    |
|weighted avg             |    307|  0.8984|N/A                                    |
|inform                   |     63|  0.8696|get_incident_status(3), connect_wifi(3)|
|create_app_user          |     40|  0.9639|N/A                                    |
|chitchat                 |     18|  0.9444|confirm(1)                             |
|get_incident_status      |     18|  0.7778|inform(2), open_incident(1)            |
|connect_wifi             |     17|  0.9189|N/A                                    |
|password_reset           |     15|  1.0000|N/A                                    |
|goodbye                  |     14|  0.8800|show_menu(1), confirm(1)               |
|out_of_scope             |     14|  0.7407|deny(2), open_incident(1)              |
|faq                      |     13|  0.8800|create_app_user(1), open_incident(1)   |
|problem_email            |     13|  1.0000|N/A                                    |
|open_incident            |     12|  0.8571|N/A                                    |
|request_biometrics_report|     12|  0.9600|N/A                                    |
|greet                    |     11|  1.0000|N/A                                    |
|help                     |     11|  0.9524|open_incident(1)                       |
|confirm                  |     11|  0.8333|chitchat(1)                            |
|deny                     |     11|  0.7826|thank(1), confirm(1)                   |
|thank                    |      8|  0.8889|N/A                                    |
|show_menu                |      6|  0.9231|N/A                                    |



# Entity Cross-Validation Results (5 folds)
|   entity   |support|f1-score|precision|recall|
|------------|------:|-------:|--------:|-----:|
|micro avg   |    132|  0.8571|   0.9000|0.8182|
|macro avg   |    132|  0.8283|   0.9106|0.7886|
|weighted avg|    132|  0.8438|   0.9122|0.8182|
|application |     58|  0.9076|   0.8852|0.9310|
|faculty     |     20|  0.5714|   1.0000|0.4000|
|wifi_network|     14|  0.9655|   0.9333|1.0000|
|course_type |     12|  0.9091|   1.0000|0.8333|
|priority    |     10|  0.8889|   1.0000|0.8000|
|role        |      9|  0.5556|   0.5556|0.5556|
|ticket_no   |      9|  1.0000|   1.0000|1.0000|



# Entity Cross-Validation Results (5 folds)
|         entity          |support|f1-score|precision|recall|
|-------------------------|------:|-------:|--------:|-----:|
|macro avg                |     31|       1|        1|     1|
|weighted avg             |     31|       1|        1|     1|
|chitchat/bot_challenge   |     10|       1|        1|     1|
|chitchat/how_are_you     |      8|       1|        1|     1|
|faq/helpdesk_availability|      8|       1|        1|     1|
|faq/dtic_info            |      5|       1|        1|     1|
