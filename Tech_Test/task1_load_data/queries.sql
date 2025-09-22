--QUERY 1
SELECT 
B.server,
COUNT(*) AS num_of_complaints,
ROUND(AVG(EXTRACT(EPOCH FROM B.ser_time::interval) / 60), 2) AS avg_call_minutes

FROM crm_call_center_logs AS B
JOIN crm_events AS A 
ON B.complaint_id = A.complaint_id
WHERE B.complaint_id IS NOT NULL
GROUP BY B.server
ORDER BY avg_call_minutes DESC
LIMIT 10;

--QUERY 2
SELECT 
	A.company_response_to_consumer,
	COUNT(*) AS num_of_complaints,
    ROUND(AVG(EXTRACT(EPOCH FROM B.ser_time::interval) / 60), 2) AS avg_duration_call_minutes,
	ROUND(AVG(A.date_sent_to_company - B.date_received)) AS avg_forwarding_days

FROM crm_call_center_logs AS B
JOIN crm_events AS A 
	ON B.complaint_id = A.complaint_id
WHERE B.complaint_id IS NOT NULL

GROUP BY A.company_response_to_consumer
ORDER BY num_of_complaints DESC;