package edu.cnm.deepdive.petamber.server.model.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.FetchType
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import jakarta.persistence.Index
import jakarta.persistence.JoinColumn
import jakarta.persistence.ManyToOne
import jakarta.persistence.Table
import jakarta.persistence.UniqueConstraint
import org.hibernate.annotations.CreationTimestamp
import kotlin.time.Instant

@Entity
@Table(
    name = "corroboration",
    uniqueConstraints = [
        UniqueConstraint(
            name = "uq_corroboration_sighting_user",
            columnNames = ["sighting_id", "user_id"]
        )
    ],
    indexes = [
        Index(columnList = "sighting_id"),
        Index(columnList = "user_id")
    ]
)
class Corroboration(

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "sighting_id", nullable = false, updatable = false)
    var sighting: Sighting,

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false, updatable = false)
    var user: UserProfile,

    @Column(name = "is_confirmed", nullable = false)
    var isConfirmed: Boolean = true,

    @Column(name = "corroboration_notes", nullable = true, length = 500)
    var corroborationNotes: String? = null

) {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "corroboration_id", nullable = false, updatable = false)
    var id: Long? = null

    @Column(nullable = false, updatable = false)
    @CreationTimestamp
    open var created: Instant? = null

}
