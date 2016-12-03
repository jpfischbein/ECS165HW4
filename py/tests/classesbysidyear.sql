SELECT COUNT(sid)
FROM Student S,
		(
		SELECT sid, SUM(s.units) as sum
		FROM Student s, Course c
		WHERE S.cid = C.cid AND C.quarter = qtr
		GROUP BY sid, year
		) U
WHERE S.sid = U.sid AND U.sum = units